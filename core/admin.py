from django.contrib import admin

from core import models


@admin.register(models.Performence)
class PerformenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name__startswith', )


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'release_year')


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_num')
