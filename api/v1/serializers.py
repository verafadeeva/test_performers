from rest_framework import serializers

from core import models


class SingerListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка исполнителей"""
    class Meta:
        model = models.Performence
        fields = ('id', 'name')


class AlbumSimpleSerializer(serializers.Serializer):
    """Сериализатор для поля albums в SingerSerializer"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    release_year = serializers.IntegerField()


class SingerSerializer(SingerListSerializer):
    """Сериализатор для одиночного отображения исполнителя"""
    albums = AlbumSimpleSerializer(many=True)

    class Meta:
        model = models.Performence
        fields = ('id', 'name', 'albums')


class SongSimpleSerializer(serializers.Serializer):
    """Сериализатор для поля songs в AlbumSerializer"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    order_num = serializers.IntegerField()


class AlbumSerializer(AlbumSimpleSerializer):
    """Сериализатор для альбомов"""
    singer = serializers.CharField(source='singer.name')
    songs = SongSimpleSerializer(many=True, required=False)


class SongSerializer(SongSimpleSerializer):
    """Сериализатор для песен"""
    album = serializers.CharField(source='album.name')
    singer = serializers.CharField(source='album.singer.name')
