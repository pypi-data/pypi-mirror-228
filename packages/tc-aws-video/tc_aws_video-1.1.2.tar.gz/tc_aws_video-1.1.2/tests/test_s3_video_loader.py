import botocore.session
from derpconf.config import Config
from thumbor.context import Context
from tornado.testing import gen_test

from fixtures.storage_fixture import IMAGE_PATH, VIDEO_PATH, IMAGE_BYTES, VIDEO_BYTES, FRAME_BYTES, s3_bucket
from tc_aws_video.loaders import s3_video_loader
from tests import S3MockedAsyncTestCase


class S3VideoLoaderTestCase(S3MockedAsyncTestCase):
    @gen_test
    def test_can_load_image(self):
        client = botocore.session.get_session().create_client('s3')
        client.create_bucket(Bucket=s3_bucket)

        client.put_object(
            Bucket=s3_bucket,
            Key=''.join(['root_path', IMAGE_PATH]),
            Body=IMAGE_BYTES,
            ContentType='image/jpeg', )

        conf = Config(
            TC_AWS_LOADER_BUCKET=s3_bucket,
            TC_AWS_LOADER_ROOT_PATH='root_path'
        )

        image = yield s3_video_loader.load(Context(config=conf), IMAGE_PATH)
        self.assertEqual(image, IMAGE_BYTES)

    @gen_test
    def test_can_load_video_first_frame(self):
        client = botocore.session.get_session().create_client('s3')
        client.create_bucket(Bucket=s3_bucket)

        client.put_object(
            Bucket=s3_bucket,
            Key=''.join(['root_path', VIDEO_PATH]),
            Body=VIDEO_BYTES,
            ContentType='video/mp4', )

        conf = Config(
            TC_AWS_LOADER_BUCKET=s3_bucket,
            TC_AWS_LOADER_ROOT_PATH='root_path'
        )

        image = yield s3_video_loader.load(Context(config=conf), VIDEO_PATH)
        self.assertEqual(image, FRAME_BYTES)
