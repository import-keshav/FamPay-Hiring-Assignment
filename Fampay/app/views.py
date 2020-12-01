import asyncio
import threading
from django import forms
from django.shortcuts import render

from rest_framework import generics, status, filters
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination

from . import models
from . import serializers


class GetVideosPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class GetVideos(generics.ListAPIView):
    """View for getting all the videos, order by latest published date."""
    renderer_classes = [JSONRenderer]
    serializer_class = serializers.VideoSerializer
    pagination_class = GetVideosPagination
    queryset = models.Video.objects.all().order_by('-publish_date_time')


class AddAPIKey(generics.CreateAPIView):
    """View for adding a new Youtube Data API Key in the database."""
    renderer_classes = [JSONRenderer]
    serializer_class = serializers.APIKeySerializer
