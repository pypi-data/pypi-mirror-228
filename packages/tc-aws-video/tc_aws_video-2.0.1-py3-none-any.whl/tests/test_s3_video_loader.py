import botocore.session
from derpconf.config import Config
from mock import patch
from thumbor.context import Context
from thumbor.loaders import LoaderResult
from tornado.testing import gen_test

from fixtures.storage_fixture import IMAGE_PATH, VIDEO_PATH, IMAGE_BYTES, VIDEO_BYTES, FRAME_BYTES, s3_bucket
from tc_aws_video.loaders import s3_video_loader
from tests import S3MockedAsyncTestCase


class S3VideoLoaderTestCase(S3MockedAsyncTestCase):
    @gen_test
    async def test_can_load_image(self):
        client = botocore.session.get_session().create_client('s3', endpoint_url='http://localhost:5000')
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

        loader_result = await s3_video_loader.load(Context(config=conf), IMAGE_PATH)
        print(loader_result.metadata)
        self.assertTrue(loader_result.successful)
        self.assertEqual(loader_result.buffer, IMAGE_BYTES)
        self.assertTrue('size' in loader_result.metadata)
        self.assertIsNone(loader_result.error)

    @gen_test
    async def test_can_load_video_first_frame(self):
        client = botocore.session.get_session().create_client('s3', endpoint_url='http://localhost:5000')
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

        loader_result = await s3_video_loader.load(Context(config=conf), VIDEO_PATH)
        print(loader_result.metadata)
        self.assertTrue(loader_result.successful)
        self.assertEqual(loader_result.buffer, FRAME_BYTES)
        self.assertTrue('size' in loader_result.metadata)
        self.assertIsNone(loader_result.error)

    @patch('thumbor.loaders.http_loader.load')
    @gen_test
    async def test_should_use_http_loader(self, load_sync_patch):
        conf = Config(TC_AWS_ENABLE_HTTP_LOADER=True)
        await s3_video_loader.load(Context(config=conf), 'http://foo.bar')
        self.assertTrue(load_sync_patch.called)

    @gen_test
    async def test_returns_404_on_no_image(self):
        conf = Config(
            TC_AWS_LOADER_BUCKET=s3_bucket,
            TC_AWS_LOADER_ROOT_PATH='root_path'
        )

        loader_result = await s3_video_loader.load(Context(config=conf), 'foo-bar.jpg')
        self.assertFalse(loader_result.successful)
        self.assertIsNone(loader_result.buffer)
        self.assertEqual(loader_result.error, LoaderResult.ERROR_NOT_FOUND)

    @gen_test
    async def test_can_validate_buckets(self):
        conf = Config(
            TC_AWS_ALLOWED_BUCKETS=['whitelist_bucket'],
            TC_AWS_LOADER_BUCKET=None,
        )

        image = await s3_video_loader.load(Context(config=conf), '/'.join([s3_bucket, IMAGE_PATH]))
        self.assertIsNone(image.buffer)

    @patch('thumbor.loaders.http_loader.load')
    @gen_test
    async def test_should_not_use_http_loader_if_not_prefixed_with_scheme(self, load_sync_patch):
        conf = Config(TC_AWS_ENABLE_HTTP_LOADER=True)
        await s3_video_loader.load(Context(config=conf), 'foo/bar')
        self.assertFalse(load_sync_patch.called)
