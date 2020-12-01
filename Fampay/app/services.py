""" This module contains services that get results from youtube and add in the database"""

import asyncio
import datetime
import threading
import time
from apiclient.discovery import build
from django.db import connections

from . import models


def youtube_search_keyword(query, max_results):
    """Fetching the latest videos for a search query using Youtube Data API.

    Args:
        query (str): search query.
        max_results(int): Maximum no of results we want in response from the Y
            Youtube Data API.

    Returns:
        results (list): List of all the videos data in dict format.
    """
    api_keys = models.APIKey.objects.filter(is_limit_over=False)

    if not len(api_keys):
        return {}

    DEVELOPER_KEY = api_keys[0]
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    try:
        youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                               developerKey=DEVELOPER_KEY)
        search_keyword = youtube_object.search().list(q=query, part="id, snippet",
                                                      maxResults=max_results).execute()

        results = search_keyword.get("items", [])
    except:
        api_keys[0].is_limit_over = True
        api_keys[0].save()
        return {}

    return results


def get_date_time_object_from_string(date_time):
    """Create a datetime object from string of date and time.

    Args:
        date_time (str): String contains date and time.

    Return:
        obj: Returns a datetime object.
    """
    return datetime.datetime.strptime(
        date_time.split('T')[0] + ' ' + date_time.split('T')[1].split('Z')[0],
        '%Y-%m-%d %H:%M:%S')


def get_desired_video_dict_from_result(result):
    """ Extract relevant values from Youtube Data API Results for video.

    Args:
        result (dict): Youtube Data API result in dictionary format.

    Returns:
        dict: Returns relevant values of result for video.
    """
    if 'videoId' in result['id']:
        video_id = result['id']['videoId']
    else:
        video_id = ''
    return {
        'title': result["snippet"]["title"],
        'description': result['snippet']['description'],
        'video_id': video_id,
        'channel_id': result['snippet']['channelId'],
        'publish_date_time': get_date_time_object_from_string(
            result['snippet']['publishedAt']),
    }


def get_video_thumbnails_from_result(result):
    """ Extract relevant values from Youtube Data API Results
    for video thumbnails.

    Args:
        result (dict): Youtube Data API result in dictionary format.

    Returns:
        list: Returns relevant values of result for video thumbnails.
    """
    return [{
        'screen_size': screen_size,
        'url':  result['snippet']['thumbnails'][screen_size]['url'],
    } for screen_size in result['snippet']['thumbnails']]


def save_video_and_thumbail_in_models(result):
    """Save video and it's thumbnails in Database.

    Args:
        result (dict): Youtube Data API result in dictionary format.
    """
    video_dict = get_desired_video_dict_from_result(result)
    video_obj = models.Video(**video_dict)
    video_obj.save()

    thumbnails = get_video_thumbnails_from_result(result)
    for thumbnail in thumbnails:
        thumbnail['video'] = video_obj
        thumbnail_obj = models.VideoThumbNail(**thumbnail)
        thumbnail_obj.save()

    # Clossing all connections before delay to overcome concurrency
    for conn in connections.all():
        conn.close()


def get_time_of_most_recent_uploaded_video():
    """Returns time of most recent uploaded video.

    Returns:
        resent_date_time (datetime): Returns datetime object.
    """
    resent_date_time = ''
    search_results = youtube_search_keyword('today news', 10)

    if search_results == {}:
        return

    for result in search_results:
        video_date_time_obj = get_date_time_object_from_string(
            result['snippet']['publishedAt'])
        save_video_and_thumbail_in_models(result)

        if not resent_date_time:
            resent_date_time = video_date_time_obj

        resent_date_time = max(resent_date_time, video_date_time_obj)
    return resent_date_time


async def search_and_add_youtube_videos_service():
    """Asynchronous function for fetching the latest videos
    for a search query and should storing it in database.
    """
    resent_date_time = get_time_of_most_recent_uploaded_video()

    while True:
        search_results = youtube_search_keyword('today news', 10)

        if search_results == {}:
            return

        for result in search_results:
            video_date_time_obj = get_date_time_object_from_string(
                result['snippet']['publishedAt'])

            if resent_date_time < video_date_time_obj:
                save_video_and_thumbail_in_models(result)
                resent_date_time = video_date_time_obj

        await asyncio.sleep(10)


def start_searching_and_adding_youtube_videos():
    """Start services for searching and adding youtube videos."""
    while True:
        api_keys = models.APIKey.objects.filter(is_limit_over=False)
        if len(api_keys):
            asyncio.run(search_and_add_youtube_videos_service())
        time.sleep(10)

THREAD = threading.Thread(target=start_searching_and_adding_youtube_videos)
