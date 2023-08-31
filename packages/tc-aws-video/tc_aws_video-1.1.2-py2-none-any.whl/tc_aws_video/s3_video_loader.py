# -*- coding: utf-8 -*-

import mimetypes
import os
import tempfile
import uuid
from urllib import unquote

import botocore.session
import subprocess32 as subprocess
from thumbor.loaders import LoaderResult
from thumbor.utils import logger
from tornado.concurrent import return_future


# Check whether the object is an image according to the object MIME type
def is_image(mime_type):
    return mime_type.startswith('image/')


# Check whether the object is a video according to the object MIME type
def is_video(mime_type):
    return mime_type.startswith('video/')


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
    aws_access_key = context.config.get('TC_AWS_LOADER_ACCESS_KEY', None)
    aws_secret_key = context.config.get('TC_AWS_LOADER_SECRET_KEY', None)
    aws_region = context.config.get('TC_AWS_REGION', None)
    aws_endpoint = context.config.get('TC_AWS_ENDPOINT', None)
    video_frame_cache_dir = context.config.get('TC_AWS_LOADER_VIDEO_FRAME_CACHE', tempfile.gettempdir())

    # Get the bucket name and object key from the url
    url_parts = url.split("/", 1)
    if len(url_parts) != 2:
        logger.error("Invalid URL format: %s", url)
        result = LoaderResult()
        result.error = "Invalid URL format"
        result.successful = False
        callback(result)
        return

    bucket, key = url_parts
    # decode the bucket and key , otherwise, chinese encode will cause 404 not found
    decode_bucket = unquote(bucket)
    decoded_key = unquote(key)

    session = botocore.session.get_session()
    s3_client = session.create_client('s3', region_name=aws_region,
                                      aws_access_key_id=aws_access_key,
                                      aws_secret_access_key=aws_secret_key,
                                      endpoint_url=aws_endpoint)

    try:
        obj = s3_client.head_object(Bucket=decode_bucket, Key=decoded_key)
        content_type = obj['ContentType']
        mime_type, _ = mimetypes.guess_type(url)
        result = LoaderResult()

        if is_image(content_type) or is_image(mime_type):
            response = s3_client.get_object(Bucket=decode_bucket, Key=decoded_key)
            result.buffer = response['Body'].read()
            result.successful = True
        elif is_video(content_type) or is_video(mime_type):
            # Accelerate the efficiency of extracting the first frame by using pre-signed url
            presigned_url = s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': decode_bucket, 'Key': decoded_key},
                                                             ExpiresIn=100)
            first_frame_path = get_video_first_frame(video_frame_cache_dir, presigned_url)
            if os.path.exists(first_frame_path):
                with open(first_frame_path, 'rb') as f:
                    result.buffer = f.read()
                    result.successful = True
                os.remove(first_frame_path)
            else:
                result.error = 'Get the first frame of vedio failed'
                result.successful = False
        else:
            result.error = 'File type not supported'
            result.successful = False
        callback(result)
    except Exception as e:
        logger.error("Error processing object: %s", e)
        result = LoaderResult()
        result.error = str(e)
        result.successful = False
        callback(result)
