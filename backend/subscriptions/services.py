from common.service_utils import update_model
from subscriptions.models import Subscription


class SubscriptionService:
    def create(self, user, subscription_arn, topic_arn, filter_policy):
        return Subscription.objects.create(
            user=user,
            subscription_arn=subscription_arn,
            topic_arn=topic_arn,
            filter_policy=filter_policy,
        )

    def delete(self, user, topic_arn):
        self.get(user, topic_arn).delete()
        pass

    def get(self, user, topic_arn):
        subscription = Subscription.objects.get(user=user, topic_arn=topic_arn)
        return subscription

    def update(self, user, topic_arn, filter_policy):
        subscription = self.get(user=user, topic_arn=topic_arn)
        return update_model(subscription, {"filter_policy": filter_policy})[0]
