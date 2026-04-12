from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils.encoding import filepath_to_uri
from urllib.parse import urljoin


class FixedStaticFilesStorage(StaticFilesStorage):
    """
    修复 StaticFilesStorage.url 方法，确保正确拼接 base_url 和文件名。
    """
    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        # 将文件路径转换为 URI 格式（去除前导斜杠）
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip("/")
        # 如果 base_url 以 '/' 开头但缺少协议，则手动拼接
        if self.base_url.startswith('/') and '://' not in self.base_url:
            # 手动拼接，避免 urljoin 的奇怪行为
            base = self.base_url.rstrip('/')
            return f"{base}/{url}" if url else base
        # 否则使用默认的 urljoin（当 base_url 包含协议时）
        return urljoin(self.base_url, url)