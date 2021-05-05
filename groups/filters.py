from .models import Group
import django_filters

class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Group
        fields = ['name']