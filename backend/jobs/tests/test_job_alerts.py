from django.test import TestCase

from companies.factories import CompanyFactory
from jobs.alerts import JobAlertsClient
from subscriptions.models import Subscription
from users.factories import UserFactory


class TestJobAlerts(TestCase):
    def setUp(self) -> None:
        self.jobAlerts = JobAlertsClient()
        topic = self.jobAlerts.create_topic("test_job_alerts")
        self.test_topic_arn = topic["TopicArn"]

    def tearDown(self) -> None:
        topics = self.jobAlerts.list_topics()

        for topic in topics["Topics"]:
            print("topic arn", topic["TopicArn"])
            self.jobAlerts.delete_topic(topic["TopicArn"])

    def test_should_create_topic_in_setUp(self):
        print("JOB ALERT TESTS")
        topics = self.jobAlerts.list_topics()

        self.assertEqual(1, len(topics["Topics"]))

    def test_should_subscribe_to_a_topic(self):
        jobseeker = UserFactory()

        subscription = self.jobAlerts.subscribe(jobseeker, self.test_topic_arn)

        self.assertEqual(1, Subscription.objects.count())
        self.assertEqual(self.test_topic_arn, subscription.topic_arn)

    def test_should_add_company_to_users_filter_policy(self):
        company_1 = CompanyFactory()
        company_2 = CompanyFactory()
        jobseeker = UserFactory()
        subscription = self.jobAlerts.subscribe(jobseeker, self.test_topic_arn)

        subscription = self.jobAlerts.add_company(
            jobseeker, company_1, self.test_topic_arn
        )
        subscription = self.jobAlerts.add_company(
            jobseeker, company_2, self.test_topic_arn
        )
        self.assertIn(company_1.id, subscription.filter_policy["company"])
        self.assertIn(company_2.id, subscription.filter_policy["company"])

    def test_should_remove_company_from_users_filter_policy(self):
        company_1 = CompanyFactory()
        company_2 = CompanyFactory()
        jobseeker = UserFactory()
        subscription = self.jobAlerts.subscribe(jobseeker, self.test_topic_arn)

        subscription = self.jobAlerts.add_company(
            jobseeker, company_1, self.test_topic_arn
        )
        subscription = self.jobAlerts.add_company(
            jobseeker, company_2, self.test_topic_arn
        )

        print("subscription:", subscription)
        subscription = self.jobAlerts.remove_company(
            jobseeker, company_1, self.test_topic_arn
        )
        self.assertNotIn(company_1.id, subscription.filter_policy["company"])
        self.assertIn(company_2.id, subscription.filter_policy["company"])

        subscription = self.jobAlerts.remove_company(
            jobseeker, company_2, self.test_topic_arn
        )
        self.assertNotIn(company_2.id, subscription.filter_policy["company"])

        print("subscription:", subscription)
