from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Performence(models.Model):
    """Модель Исполнитель"""
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return f'{self.name}'


class Album(models.Model):
    """Модель Альбом"""
    name = models.CharField(max_length=100)
    singer = models.ForeignKey(
        Performence,
        on_delete=models.CASCADE,
        related_name='albums',
    )
    release_year = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('name', 'singer'),
                                    name='unique_album_singer')
        ]

    def clean(self):
        cur_year = timezone.now().year
        if self.release_year > cur_year:
            raise ValidationError('Год релиза альбома еще не наступил')

    def __str__(self) -> str:
        return f'{self.name}: {self.singer}'


class Song(models.Model):
    """Модель Песня"""
    name = models.CharField(max_length=100)
    order_num = models.PositiveSmallIntegerField()
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='songs',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('name', 'order_num', 'album'),
                                    name='unique_song_in_album')
        ]

    def __str__(self) -> str:
        return f'{self.order_num}.{self.name} - {self.album.name}'
