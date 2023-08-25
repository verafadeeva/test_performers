from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from core import models
from api.v1 import serializers, services


class SingerViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """Viewset для отображения исполнителей"""
    queryset = models.Performence.objects.all().prefetch_related('albums')
    serializer_class = serializers.SingerListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.SingerSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        singer = services.singer_create(**serializer.validated_data)
        return Response(data={'id': singer.id, 'name': singer.name},
                        status=status.HTTP_201_CREATED,
                        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        singer = services.singer_update(album=instance,
                                        **serializer.validated_data,
                                        )

        return Response(data={'id': singer.id, 'name': singer.name},
                        status=status.HTTP_200_OK,
                        )

    def destroy(self, request, *args, **kwargs):
        singer = self.get_object()
        services.singer_destroy(singer=singer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet
                   ):
    """Viewset для отображения альбомов"""
    queryset = models.Album.objects.all().select_related(
        'singer').prefetch_related('songs')
    serializer_class = serializers.AlbumSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = services.album_create(**serializer.validated_data)
        return Response(data={'id': album.id, 'name': album.name},
                        status=status.HTTP_201_CREATED,
                        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = services.album_update(album=instance,
                                      **serializer.validated_data,
                                      )

        return Response(data={'id': album.id, 'name': album.name},
                        status=status.HTTP_200_OK,
                        )

    def destroy(self, request, *args, **kwargs):
        album = self.get_object()
        services.album_destroy(album=album)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для отображения песен"""
    queryset = models.Song.objects.all().select_related(
        'album').select_related('album__singer')
    serializer_class = serializers.SongSerializer
