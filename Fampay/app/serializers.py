"""This module contains serializers for Video and VideoThumbNail models."""

from rest_framework import serializers

from . import models
from . import services

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video Model."""
    thumbnails = serializers.SerializerMethodField()

    def get_thumbnails(self, obj):
        """Returns all thumbnails of the video.

        Args:
            obj: Video Object

        Returns:
            list: List of thumbnails dict. 
        """
        return [
            VideoThumbNailSerializer(thumbnail).data
                for thumbnail in models.VideoThumbNail.objects.filter(video=obj)]

    class Meta:
        model = models.Video
        fields = '__all__'


class VideoThumbNailSerializer(serializers.ModelSerializer):
    """Serializer for VideoThumbNail Model."""
    class Meta:
        model = models.VideoThumbNail
        fields = '__all__'


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for APIKey Model."""
    class Meta:
        model = models.APIKey
        fields = '__all__'