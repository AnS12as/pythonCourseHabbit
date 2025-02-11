import django_filters

from .models import Habit


class HabitFilter(django_filters.FilterSet):
    class Meta:
        model = Habit
        fields = {
            "is_public": ["exact"],
            "time": ["gte", "lte"],
        }
