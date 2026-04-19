from django.contrib.staticfiles.storage import StaticFilesStorage
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from urllib.parse import urljoin


class FixedStaticFilesStorage(StaticFilesStorage):
    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip("/")
        if self.base_url.startswith('/') and '://' not in self.base_url:
            base = self.base_url.rstrip('/')
            return f"{base}/{url}" if url else base
        return urljoin(self.base_url, url)


class FixedMediaFilesStorage(FileSystemStorage):
    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip("/")
        if self.base_url.startswith('/') and '://' not in self.base_url:
            base = self.base_url.rstrip('/')
            return f"{base}/{url}" if url else base
        return urljoin(self.base_url, url)