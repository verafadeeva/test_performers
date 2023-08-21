from rest_framework import serializers

from core import models


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Performence
        fields = ('id', 'name')


class SingerObjectSerializer(SingerSerializer):
    albums = serializers.SerializerMethodField

    class Meta:
        model = models.Performence
        fields = ('id', 'name', 'albums')

    def get_albums(self, obj):
        albums = obj.albums.all()
        serializer = AlbumSimpleSerializer(albums, many=True)
        return serializer.data


class AlbumSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ('id', 'name', 'release_year')
