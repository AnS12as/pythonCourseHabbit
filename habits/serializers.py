from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        if data.get("duration", 0) > 120:
            raise serializers.ValidationError("Duration cannot exceed 120 seconds.")
        if data.get("reward") and data.get("linked_habit"):
            raise serializers.ValidationError(
                "Either reward or linked habit must be set, not both."
            )
        if data.get("is_pleasant") and (data.get("reward") or data.get("linked_habit")):
            raise serializers.ValidationError(
                "Pleasant habits cannot have a reward or linked habit."
            )
        if data.get("frequency", 1) < 1 or data.get("frequency") > 7:
            raise serializers.ValidationError("Frequency must be between 1 and 7 days.")
        return data


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "frequency",
            "reward",
            "duration",
            "is_public",
        ]
        read_only_fields = ["user"]
