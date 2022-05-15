from .models import Factory
from django.db.models import Q
import django_filters


class FactoryFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")

    class Meta:
        model = Factory
        fields = ['query']

    def universal_search(self, queryset, name, value):
        return Factory.objects.filter(
            Q(factory_name__icontains=value))
