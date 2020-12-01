from django.contrib import admin

from . import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
	list_display = [field.name for field in models.Video._meta.fields]
	search_fields = ('publish_date_time', 'video_id', 'channel_id',
		'title', 'id')
	list_filter = ('publish_date_time',)


@admin.register(models.VideoThumbNail)
class VideoThumbNailAdmin(admin.ModelAdmin):
	list_display = [field.name for field in models.VideoThumbNail._meta.fields]
	search_fields = ('video__title', 'video__channel_id', 'video__video_id',
		'video__publish_date_time', 'video__id', 'id')
	list_filter = ('video', 'screen_size')


@admin.register(models.APIKey)
class APIKeyAdmin(admin.ModelAdmin):
	list_display = [field.name for field in models.APIKey._meta.fields]
