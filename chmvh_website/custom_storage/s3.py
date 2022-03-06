from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage

from chmvh_website.settings import S3_MEDIA_BUCKET, S3_STATIC_BUCKET


class MediaStorage(S3Boto3Storage):
    bucket_name = S3_MEDIA_BUCKET


class StaticStorage(S3ManifestStaticStorage):
    bucket_name = S3_STATIC_BUCKET
