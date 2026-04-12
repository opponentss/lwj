from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # 确保使用自定义静态文件存储
        from django.contrib.staticfiles.storage import staticfiles_storage
        from blog.storage import FixedStaticFilesStorage
        # 如果当前存储不是自定义存储，则替换
        if not isinstance(staticfiles_storage._wrapped, FixedStaticFilesStorage):
            staticfiles_storage._wrapped = FixedStaticFilesStorage()
