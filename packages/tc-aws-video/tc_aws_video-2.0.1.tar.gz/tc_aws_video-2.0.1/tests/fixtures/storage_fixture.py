# coding: utf-8

# Copyright (c) 2015, thumbor-community
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

from os.path import join, abspath, dirname

from thumbor.context import ServerParameters

s3_bucket = 'thumbor-images-test'

IMAGE_URL = 'loader-test/some/image_%s.jpg'
IMAGE_PATH = join(abspath(dirname(__file__)), 'image.jpg')
VIDEO_PATH = join(abspath(dirname(__file__)), 'sample.mp4')
FRAME_PATH = join(abspath(dirname(__file__)), 'sample.jpg')

with open(IMAGE_PATH, 'rb') as img:
    IMAGE_BYTES = img.read()

with open(FRAME_PATH, 'rb') as fr:
    FRAME_BYTES = fr.read()

with open(VIDEO_PATH, 'rb') as vdo:
    VIDEO_BYTES = vdo.read()


def get_server(key=None):
    server_params = ServerParameters(8888, 'localhost', 'thumbor.conf.debug', None, 'info', None)
    server_params.security_key = key
    return server_params
