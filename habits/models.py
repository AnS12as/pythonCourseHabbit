from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings  # ✅ Используем кастомного пользователя


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
        - frequency: Частота выполнения привычки (дни, от 1 до 7).
        - reward: Награда за выполнение привычки.
        - duration: Длительность выполнения привычки (максимум 120 минут).
        - is_public: Привычка является публичной.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")  # ✅
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    linked_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="linked_to",
        verbose_name="Связанная привычка",
    )
    frequency = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message="Частота должна быть минимум 1 день."),
            MaxValueValidator(7, message="Частота не может превышать 7 дней."),
        ],
        verbose_name="Частота",
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Награда"
    )
    duration = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(120, message="Длительность не может превышать 120 минут."),
        ],
        verbose_name="Длительность",
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def clean(self):
        """
        Выполняет валидацию данных перед сохранением.
        """
        if self.reward and self.linked_habit:
            raise ValidationError(
                "Можно задать либо награду, либо связанную привычку, но не обе одновременно."
            )
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError(
                "Приятные привычки не могут иметь награду или связанную привычку."
            )

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")  # ✅
    telegram_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # ✅
def manage_user_profile(sender, instance, created, **kwargs):
    """
    Управляет созданием и сохранением профиля пользователя.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
