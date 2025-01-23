from django.db import models
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="linked_to",
    )
    frequency = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.duration > 120:
            raise ValidationError("Duration cannot exceed 120 seconds.")
        if self.reward and self.linked_habit:
            raise ValidationError(
                "Either reward or linked habit must be set, not both."
            )
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError(
                "Pleasant habits cannot have a reward or linked habit."
            )
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError("Frequency must be between 1 and 7 days.")

    def __str__(self):
        return f"{self.action} at {self.time}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    telegram_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
