from django.contrib.staticfiles.storage import staticfiles_storage
print('location:', staticfiles_storage.location)
print('base_url:', staticfiles_storage.base_url)
url = staticfiles_storage.url('blog/css/style.css')
print('url:', url)
print('url type:', type(url))
# 检查是否调用了父类方法
from django.core.files.storage import Storage
print('Parent class:', staticfiles_storage.__class__.__bases__)
# 手动拼接
if staticfiles_storage.base_url and not url.startswith(staticfiles_storage.base_url):
    print('WARNING: base_url not prefixed')
    print('Expected:', staticfiles_storage.base_url + 'blog/css/style.css')
else:
    print('Base_url prefixed correctly')