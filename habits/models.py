from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Habit(models.Model):
    """
    Модель для привычек.

    Поля:
        - user: Владелец привычки.
        - place: Место выполнения привычки.
        - time: Время выполнения.
        - action: Описание действия.
        - is_pleasant: Привычка является приятной.
        - linked_habit: Связанная привычка.
        - frequency: Частота выполнения привычки (дни).
        - reward: Награда за выполнение привычки.
        - duration: Длительность выполнения привычки (в минутах).
        - is_public: Привычка является публичной.
    """
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
        """
        Выполняет валидацию данных перед сохранением.
        """
        if self.duration > 120:
            raise ValidationError("Длительность не может превышать 120 минут.")
        if self.reward and self.linked_habit:
            raise ValidationError(
                "Можно задать либо награду, либо связанную привычку, но не обе одновременно."
            )
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError(
                "Приятные привычки не могут иметь награду или связанную привычку."
            )
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError("Частота должна быть в пределах от 1 до 7 дней.")

    def save(self, *args, **kwargs):
        """
        Сохраняет объект, предварительно вызывая метод clean().
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} at {self.time}"


class Profile(models.Model):
    """
    Модель профиля пользователя.

    Поля:
        - user: Связанный пользователь.
        - telegram_id: ID в Telegram.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    telegram_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создает профиль пользователя при создании нового пользователя.
    """
    if created and not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет изменения в профиле пользователя.
    """
    if hasattr(instance, "profile"):
        instance.profile.save()

