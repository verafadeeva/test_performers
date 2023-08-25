from typing import Dict, List, Union

from django.db import transaction
from django.core import exceptions as django_exceptoins

from core.models import Album, Performence, Song


@transaction.atomic
def singer_create(*, name: str) -> Performence:
    """Создает и возвращает объект класса Performence"""
    singer = Performence(name=name)
    singer.full_clean()
    singer.save()
    return singer


def singer_get(name: str) -> Performence:
    """Получает объект класса Performence"""
    singer = Performence.objects.get(name=name)
    return singer


@transaction.atomic
def singer_update(*, singer: Performence, name: str = '',) -> Performence:
    """Update существующего объекта класса Performence"""
    name = singer.name if name == '' else name
    singer.name = name
    return singer


def singer_destroy(*, singer: Performence) -> None:
    """Удаляет объект класса Album из бд"""
    singer.delete()


@transaction.atomic
def song_create(*, name: str, order_num: int, album: Album) -> Song:
    song = Song(name=name,
                order_num=order_num,
                album=album)
    """Создает и возвращает объект класса Song"""
    song.full_clean()
    song.save()
    return song


def get_songs(songs: List[Dict[str, str]], album: Album) -> List[Song]:
    """
    Принимает список песен структуры
    songs = [
        {"name": str,
        "order_num": int}
        ]
    Получает из бд объекты или (если объект не найден) вызывает функцию
    song_create().
    """

    songs_obj = set()
    for song in songs:
        try:
            song = Song.objects.get(name=song.get('name'), album=album)
        except django_exceptoins.ObjectDoesNotExist:
            song = song_create(name=song.get('name'),
                               order_num=song.get('order_num'),
                               album=album,
                               )
        songs_obj.add(song)
    return list(songs_obj)


@transaction.atomic
def album_create(*,
                 name: str,
                 singer: Dict[str, str],
                 release_year: int,
                 songs: Union[List[Dict[str, str]], None] = None) -> Album:
    """Сщдает и возвращает объект класса Album"""
    singer_name = singer.get('name').title()
    try:
        singer_obj = Performence.objects.get(name=singer_name)
    except django_exceptoins.ObjectDoesNotExist:
        singer_obj = singer_create(name=singer_name)

    album = Album(name=name,
                  singer=singer_obj,
                  release_year=release_year)

    album.full_clean()
    album.save()

    if songs is not None:
        for song in songs:
            song_create(name=song.get('name'),
                        order_num=song.get('order_num'),
                        album=album,
                        )

    return album


@transaction.atomic
def album_update(*,
                 album: Album,
                 name: str = '',
                 singer: Union[Dict[str, str], None] = None,
                 release_year: Union[int, None] = None,
                 songs: Union[List[Dict[str, str]], None] = None) -> Album:
    """Update существующего объекта класса Album"""

    name = album.name if name == '' else name
    singer = album.singer if singer is None else singer_get(singer.get('name'))
    release_year = album.release_year if release_year is None else release_year

    if songs:
        songs = get_songs(songs=songs, album=album)
        album.songs.set(songs)

    album.name = name
    album.singer = singer
    album.release_year = release_year
    return album


def album_destroy(*, album: Album) -> None:
    """Удаляет объект класса Album из бд"""
    album.delete()
