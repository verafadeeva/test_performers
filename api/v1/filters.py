from django_filters import rest_framework as filters
from core import models


class SongFilter(filters.FilterSet):
    singer = filters.ModelChoiceFilter(
        field_name='album__singer',
        to_field_name='name',
        queryset=models.Performence.objects.all()
    )

    class Meta:
        model = models.Song
        fields = ['album', 'singer']
