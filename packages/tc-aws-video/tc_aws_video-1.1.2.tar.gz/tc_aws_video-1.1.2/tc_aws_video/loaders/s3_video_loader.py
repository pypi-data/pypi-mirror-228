# -*- coding: utf-8 -*-

import mimetypes
import os
import tempfile
import uuid

import subprocess32 as subprocess
import thumbor.loaders.http_loader as http_loader
from tc_aws.loaders.s3_loader import HandleDataFunc
from thumbor.loaders import LoaderResult
from thumbor.utils import logger
from tornado.concurrent import return_future

from tc_aws_video.aws.bucket import Bucket
from . import *


# Check whether the object is an image according to the object MIME type
def is_image(mime_type):
    return not (mime_type is None) and mime_type.startswith('image/')


# Check whether the object is a video according to the object MIME type
def is_video(mime_type):
    return not (mime_type is None) and mime_type.startswith('video/')


# Get the video first frame from an accessible url
def get_video_first_frame(temp_path, video_url):
    output_path = os.path.join(temp_path, '{}.jpg'.format(uuid.uuid4()))
    command = [
        'ffmpeg',
        '-y', '-i',
        video_url,
        '-ss', '00:00:00.000',
        '-vframes', '1',
        '-f', 'image2',
        output_path
    ]
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(
            command,
            stdout=devnull,
            stderr=devnull,
        )
        process.wait()

    return output_path


@return_future
def load(context, url, callback):
    """
    Loads image
    :param Context context: Thumbor's context
    :param string url: Path to load
    :param callable callback: Callback method once done
    """
    if _use_http_loader(context, url):
        http_loader.load_sync(context, url, callback, normalize_url_func=http_loader._normalize_url)
        return

    mime_type, _ = mimetypes.guess_type(url)
    bucket, key = _get_bucket_and_key(context, url)

    # Validate the allowed bucket
    if not _validate_bucket(context, bucket):
        result = LoaderResult(successful=False,
                              error=LoaderResult.ERROR_NOT_FOUND)
        callback(result)
        return

    # Get the required aws config info.
    aws_access_key = context.config.get('TC_AWS_LOADER_ACCESS_KEY', None)
    aws_region = context.config.get('TC_AWS_REGION', None)
    aws_endpoint = context.config.get('TC_AWS_ENDPOINT', None)
    aws_secret_key = context.config.get('TC_AWS_LOADER_SECRET_KEY', None)
    video_frame_cache_dir = context.config.get('TC_AWS_LOADER_VIDEO_FRAME_CACHE', tempfile.gettempdir())

    # If you cannot guess the mime type, then get content type from bucket stat info.
    is_img = is_image(mime_type)
    is_vdo = is_video(mime_type)
    if mime_type is None:
        content_type_future = Bucket(bucket, aws_region, aws_endpoint).stat(key)
        content_type = content_type_future.result()
        if is_image(content_type):
            is_img = True
        elif is_video(content_type):
            is_vdo = True

    # If is image loading request, fallback to use tc-aws like mode.
    if is_img:
        loader = Bucket(bucket, aws_region, aws_endpoint)
        handle_data = HandleDataFunc.as_func(key,
                                             callback=callback,
                                             bucket_loader=loader,
                                             max_retry=context.config.get('TC_AWS_MAX_RETRY'))
        loader.get(key, callback=handle_data)
        return

    # Cut the first flame
    result = LoaderResult()
    if is_vdo:
        pre_signed_url_future = Bucket(bucket, aws_region, aws_endpoint).get_url(key)
        first_frame_path = get_video_first_frame(video_frame_cache_dir, pre_signed_url_future.result())
        if os.path.exists(first_frame_path):
            with open(first_frame_path, 'rb') as f:
                result.buffer = f.read()
                result.successful = True
            os.remove(first_frame_path)
            callback(result.buffer)
        else:
            result.error = 'Get the first frame of vedio failed'
            result.successful = False
            callback(result)
        return

    # Fallback errors.
    logger.error("Error processing object: %s %s", url, key)
    result.error = LoaderResult.ERROR_NOT_FOUND
    result.successful = False
    callback(result)
