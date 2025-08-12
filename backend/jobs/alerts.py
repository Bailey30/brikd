import boto3
from django.db.models import F
from django.contrib.gis.measure import D

from common.utils import create_gis_point
from users.models import User


class JobAlerts:
    session = boto3.Session(
        aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1"
    )

    # TODO: change url for production
    sns = session.client(
        "sns", endpoint_url="http://localstack:4566", region_name="us-east-1"
    )

    def subscribe(self):
        # Subscribe to alerts from a company.
        # Need the topic arn and the user phone number.

        # response = client.subscribe(
        #     TopicArn="string",
        #     Protocol="string",
        #     Endpoint="string",
        #     Attributes={"string": "string"},
        #     ReturnSubscriptionArn=True | False,
        # )

        pass

    def unsubscribe(self):
        pass

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
        #             "StringValue": "string",
        #             "BinaryValue": b"bytes",
        #         }
        #     },
        #     MessageDeduplicationId="string",
        #     MessageGroupId="string",
        # )

        pass

    def publish_distance_topic(self, job):
        # Send messages to users within radius of created job.
        # Filter users distance to job.

        users = User.objects.all()
        point = create_gis_point(job.site.coordinates)
        recipients = users.filter(distance_alerts=True).filter(
            search_postcode_coordinates__distance_lte=(point, D(mi=F("alert_radius")))
        )

        response = self.sns.create_topic(Name="MyTopic")
        print(f"Topic ARN: {response['TopicArn']}")

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

    def create_topic(self):
        # When a company is created, create a topic so users can
        # subscribe to alerts from that company.

        # response = client.create_topic(
        #     Name="string",
        #     Attributes={"string": "string"},
        #     Tags=[
        #         {"Key": "string", "Value": "string"},
        #     ],
        #     DataProtectionPolicy="string",
        # )

        pass
