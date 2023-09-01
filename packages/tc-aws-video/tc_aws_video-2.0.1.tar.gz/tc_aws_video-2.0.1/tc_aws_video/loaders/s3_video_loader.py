# -*- coding: utf-8 -*-
import mimetypes
import os
import tempfile
import uuid
from datetime import datetime
from urllib.parse import unquote

import aiofiles
import subprocess32 as subprocess
import thumbor.loaders.http_loader as http_loader
from botocore.exceptions import ClientError
from dateutil.tz import tzutc
from thumbor.loaders import LoaderResult
from thumbor.utils import logger

from tc_aws_video.aws.bucket import Bucket


async def load(context, url):
    """
    Loads image
    :param Context context: Thumbor's context
    :param string url: Path to load
    """
    if _use_http_loader(context, url):
        return await http_loader.load(context, url)

    mime_type, _ = mimetypes.guess_type(url)
    bucket, key = _get_bucket_and_key(context, url)

    # Validate the allowed bucket
    if not _validate_bucket(context, bucket):
        result = LoaderResult(successful=False,
                              error=LoaderResult.ERROR_NOT_FOUND)
        return result

    # Get the required aws config info.
    aws_region = context.config.get('TC_AWS_REGION', None)
    aws_endpoint = context.config.get('TC_AWS_ENDPOINT', None)
    video_frame_cache_dir = context.config.get('TC_AWS_LOADER_VIDEO_FRAME_CACHE', tempfile.gettempdir())

    # If you cannot guess the mime type, then get content type from bucket stat info.
    is_img = _is_image(mime_type)
    is_vdo = _is_video(mime_type)

    if mime_type is None:
        try:
            content_type = await Bucket(bucket, aws_region, aws_endpoint).stat(key)
            if _is_image(content_type):
                is_img = True
            elif _is_video(content_type):
                is_vdo = True
        except ClientError as err:
            logger.error(
                "ERROR heading image from S3 {0}: {1}".
                format(key, str(err.response)))
            return _err_result(err)

    # If is image loading request, fallback to use tc-aws like mode.
    result = LoaderResult()
    if is_img:
        loader = Bucket(
            bucket,
            aws_region,
            aws_endpoint,
            context.config.get('TC_AWS_MAX_RETRY')
        )
        try:
            file_key = await loader.get(key)
        except ClientError as err:
            logger.error(
                "ERROR retrieving image from S3 {0}: {1}".
                format(key, str(err.response)))

            return _err_result(err)

        result.successful = True
        async with file_key['Body'] as stream:
            result.buffer = await stream.read()

        result.metadata.update(
            size=file_key['ContentLength'],
            updated_at=file_key['LastModified'],
        )

        return result

    # Cut the first flame
    if is_vdo:
        loader = Bucket(
            bucket,
            aws_region,
            aws_endpoint,
            context.config.get('TC_AWS_MAX_RETRY')
        )
        try:
            pre_signed_url = await loader.get_url(key)
        except ClientError as err:
            logger.error(
                "ERROR get image pre sign url from S3 {0}: {1}".
                format(key, str(err.response)))
            return _err_result(err)
        first_frame_path = _get_video_first_frame(video_frame_cache_dir, pre_signed_url)
        if os.path.exists(first_frame_path):
            file_size = os.path.getsize(first_frame_path)
            async with aiofiles.open(first_frame_path, mode='rb') as f:
                result.buffer = await f.read()
            result.successful = True
            result.metadata.update(
                size=file_size,
                updated_at=datetime.now(tzutc()),
            )
            os.remove(first_frame_path)
        else:
            logger.error("Get the first frame of vedio failed: [url - %s]", pre_signed_url)
            result.error = LoaderResult.ERROR_UPSTREAM
            result.successful = False
        return result

    # Fallback errors.
    logger.error("Error processing object: %s %s", url, key)
    result.error = LoaderResult.ERROR_BAD_REQUEST
    result.successful = False
    return result


def _err_result(err):
    """
    Dealing the error result to format the LoaderResult
    :param ClientError err: request mime type.
    :return: The loaderResult format from the ClientError.
    :rtype: LoaderResult
    """
    result = LoaderResult(successful=False)

    if not err.response:
        result.error = LoaderResult.ERROR_UPSTREAM
        return result

    status_code = err.response.get('ResponseMetadata', {}).get('HTTPStatusCode')

    if status_code == 404:
        result.error = LoaderResult.ERROR_NOT_FOUND
        return result

    result.error = LoaderResult.ERROR_UPSTREAM
    return result


# Check whether the object is an image according to the object MIME type
def _is_image(mime_type):
    """
    Check whether the mime type is image.
    :param string mime_type: request mime type.
    :return: Whether the request object mime is image.
    :rtype: bool
    """
    return not (mime_type is None) and mime_type.startswith('image/')


# Check whether the object is a video according to the object MIME type
def _is_video(mime_type):
    """
    Check whether the mime type is video.
    :param string mime_type: request mime type.
    :return: Whether the request object mime is video.
    :rtype: bool
    """
    return not (mime_type is None) and mime_type.startswith('video/')


# Get the video first frame from an accessible url
def _get_video_first_frame(temp_path, video_url):
    """
    Get the first frame from video.
    :param string temp_path: the cache pic store path.
    :param string video_url: the url will be read by ffmpeg.
    :return: The first frame save path
    :rtype: string
    """
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


def _use_http_loader(context, url):
    """
    Should we use HTTP Loader with given path? Based on configuration as well.
    :param Context context: Thumbor's context
    :param string url: URL to analyze
    :return: Whether we should use HTTP Loader or not
    :rtype: bool
    """
    enable_http_loader = context.config.get('TC_AWS_ENABLE_HTTP_LOADER', default=False)
    return enable_http_loader and url.startswith('http')


def _get_bucket_and_key(context, url):
    """
    Returns bucket and key from url
    :param Context context: Thumbor's context
    :param string url: The URL to parse
    :return: A tuple with the bucket and the key detected
    :rtype: tuple
    """
    url = unquote(url)

    bucket = context.config.get('TC_AWS_LOADER_BUCKET')
    if not bucket:
        bucket = _get_bucket(url)
        url = '/'.join(url.lstrip('/').split('/')[1:])

    key = _get_key(url, context)

    return bucket, key


def _get_bucket(url):
    """
    Retrieves the bucket based on the URL
    :param string url: URL to parse
    :return: bucket name
    :rtype: string
    """
    url_by_piece = url.lstrip("/").split("/")

    return url_by_piece[0]


def _get_key(path, context):
    """
    Retrieves key from path
    :param string path: Path to analyze
    :param Context context: Thumbor's context
    :return: Extracted key
    :rtype: string
    """
    root_path = context.config.get('TC_AWS_LOADER_ROOT_PATH')
    return '/'.join([root_path, path]) if root_path != '' else path


def _validate_bucket(context, bucket):
    """
    Checks that bucket is allowed
    :param Context context: Thumbor's context
    :param string bucket: Bucket name
    :return: Whether bucket is allowed or not
    :rtype: bool
    """
    allowed_buckets = context.config.get('TC_AWS_ALLOWED_BUCKETS', default=None)
    return not allowed_buckets or bucket in allowed_buckets
