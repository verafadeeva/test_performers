from rest_framework import generics, viewsets

from core import models
from api.v1 import serializers


class SingerViewSet(viewsets.ModelViewSet):
    queryset = models.Performence.objects.all().prefetch_related('albums')
    serializer_class = serializers.SingerSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.SingerObjectSerializer
        return super().get_serializer_class()
