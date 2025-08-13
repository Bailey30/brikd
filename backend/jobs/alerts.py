import json
import boto3
from django.db.models import F
from django.contrib.gis.measure import D
from django.http import response

from common.utils import create_gis_point
from companies.models import Company
from subscriptions.models import Subscription
from subscriptions.services import SubscriptionService
from users.models import User


class JobAlertsClient:
    session = boto3.Session(
        aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1"
    )

    # TODO: change url for production
    sns = session.client(
        "sns", endpoint_url="http://localstack:4566", region_name="us-east-1"
    )

    def subscribe(self, user: User, topic_arn) -> Subscription:
        """
        Subscribe to a topic.
        Initially the main job alert topic.
        """

        # TODO: subscribe users to main job alert topic on creation? or when the turn alerts on?
        # then update when they choose to subscribe to a company.

        # user_subscription_arn = UserSubscription.objects.create(user=user, topic=topic)

        filter_policy = {"company": [""]}

        response = self.sns.subscribe(
            TopicArn=topic_arn,
            Protocol="sms",
            Endpoint=user.phone_number,
            Attributes={"FilterPolicy": json.dumps(filter_policy)},
            ReturnSubscriptionArn=True | False,
        )

        subscription_arn = response["SubscriptionArn"]

        subscription = SubscriptionService().create(
            user, subscription_arn, topic_arn, filter_policy
        )

        return subscription

    def unsubscribe(self, user, topic_arn):
        """
        Deletes the subscription from SNS and the database. Shouldnt need to do this really.
        Remove companies from the subscription instead.
        """
        subscription = SubscriptionService().get(user, topic_arn)
        self.sns.unsubscribe(SubscriptionArn=subscription.subscription_arn)
        SubscriptionService().delete(user, topic_arn)

        pass

    def add_company(self, user, company, topic_arn):
        subscription = SubscriptionService().get(user, topic_arn)
        filter_policy = subscription.filter_policy
        companies = filter_policy["company"]
        companies.append(company.id)
        updated_filter_policy = {"company": companies}

        self.sns.set_subscription_attributes(
            SubscriptionArn=subscription.subscription_arn,
            AttributeName="FilterPolicy",
            AttributeValue=json.dumps(updated_filter_policy),
        )

        subscription = SubscriptionService().update(
            user, topic_arn, updated_filter_policy
        )
        return subscription

    def remove_company(self, user, company, topic_arn):
        subscription = SubscriptionService().get(user, topic_arn)
        filter_policy = subscription.filter_policy
        companies = filter_policy["company"]
        companies.remove(company.id)
        print("companies:", companies)

        updated_filter_policy = {"company": companies}
        print("updated_filter_policy:", updated_filter_policy)

        self.sns.set_subscription_attributes(
            SubscriptionArn=subscription.subscription_arn,
            AttributeName="FilterPolicy",
            AttributeValue=str(json.dumps(updated_filter_policy)),
        )
        subscription = SubscriptionService().update(
            user, topic_arn, updated_filter_policy
        )

        return subscription

    def publish_job_topic(self, job):
        # Send messages when job is created by company.
        # Need some way to make sure they dont get two messages if they have subscribed
        # to the job and the distance.

        # TODO: job topic arn saved to job.

        # response = client.publish(
        #     TopicArn="string",
        #     TargetArn="string",
        #     PhoneNumber="string",
        #     Message="string",
        #     Subject="string",
        #     MessageStructure="string",
        #     MessageAttributes={
        #         "string": {
        #             "DataType": "string",
        #             "StringValue": "string", company.id + "_alert"
        #         }
        #     },
        #     MessageDeduplicationId="string",
        #     MessageGroupId="string",
        # )

        response = self.sns.publish(
            TopicArn=topic_arn,
            Message=job_data[
                "description"
            ],  # Job description or any other relevant message
            MessageAttributes={
                "company": {"DataType": "String", "StringValue": company.id}
            },
        )

    def publish_distance_topic(self, job):
        # Send messages to users within radius of created job.
        # Filter users distance to job.

        users = User.objects.all()
        point = create_gis_point(job.site.coordinates)
        recipients = users.filter(distance_alerts=True).filter(
            search_postcode_coordinates__distance_lte=(point, D(mi=F("alert_radius")))
        )

        # ?? do you need to create a topic here at all.
        # could just publish to phone numbers.
        response = self.sns.create_topic(Name="MyTopic")
        print(f"Topic ARN: {response['TopicArn']}")

        # what is the right way to handle this topic and publishing message
        response = self.sns.publish(
            TopicArn=response["TopicArn"],
            PhoneNumber="+447533617685",
            Message="SNS Message",
        )

        print("Text response", response)

        # TODO:
        # text people where job is within alert radius and they have alerts activated
        # update user (jobseeker) model
        # create ability to subscribe to companies
        # email alerts

    def create_topic(self, topic_name):
        # When a company is created, create a topic so users can
        # subscribe to alerts from that company.

        # response = self.sns.create_topic(
        #     Name=company.id + "_alerts",
        # )

        # alternattively, instead of creating a topic per company you could send a message to one central
        # "job-alert" topic witho
        response = self.sns.create_topic(Name=topic_name)

        return response

    def delete_topic(self, topic_arn):
        self.sns.delete_topic(TopicArn=topic_arn)

    def list_topics(self):
        return self.sns.list_topics()
