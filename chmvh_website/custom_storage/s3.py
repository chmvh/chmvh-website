from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage

from django.conf.settings import S3_MEDIA_BUCKET, S3_STATIC_BUCKET


class MediaStorage(S3Boto3Storage):
    bucket_name = S3_MEDIA_BUCKET


class StaticStorage(S3ManifestStaticStorage):
    bucket_name = S3_STATIC_BUCKET
    default_acl = 'public-read'


class CachedStaticStorage(StaticStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_storage = get_storage_class("compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        self.local_storage._save(name, content)
        super().save(name, self.local_storage._open(name))
        return name
