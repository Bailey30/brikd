from django.db import models


from django.db import models
from django.conf import settings

from users.models import User  # Assuming your user model is the default User model


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    subscription_arn = models.CharField(
        max_length=255
    )  # Store the SubscriptionArn (unique identifier for the subscription)
    topic_arn = models.CharField(
        max_length=255
    )  # Store the TopicArn (the topic user is subscribed to)
    filter_policy = models.JSONField(
        default=dict
    )  # Store the filter policy (as a JSON object)

    def __str__(self):
        return f"Subscription for {self.user.profile.email} on {self.topic_arn}. Filter_policy: {self.filter_policy}"

    class Meta:
        unique_together = [
            "user",
            "topic_arn",
        ]  # Ensure each user can only subscribe once to each topic
