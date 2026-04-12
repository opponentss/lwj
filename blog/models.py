from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdownx.models import MarkdownxField


class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100, verbose_name="分类名称")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL标识")
    description = models.TextField(blank=True, verbose_name="描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = "文章分类"
        ordering = ['name']

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        """获取分类的URL"""
        from django.urls import reverse
        return reverse('category_detail', args=[self.slug])


class Article(models.Model):
    """文章模型"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '归档'),
    )

    title = models.CharField(max_length=200, verbose_name="标题")
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="URL标识")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者", related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="分类", related_name='articles')
    content = MarkdownxField(verbose_name="内容")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="摘要")
    cover_image = models.ImageField(upload_to='articles/covers/%Y/%m/%d/', blank=True, null=True, verbose_name="封面图")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="状态")
    views = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    likes = models.PositiveIntegerField(default=0, verbose_name="点赞数")
    published_at = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['author', 'published_at']),
            models.Index(fields=['category', 'published_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """获取文章的绝对URL"""
        from django.urls import reverse
        return reverse('article_detail', args=[self.slug])

    def increase_views(self):
        """原子操作增加阅读量，避免竞争条件"""
        from django.db.models import F
        Article.objects.filter(id=self.id).update(views=F('views') + 1)
        self.refresh_from_db()

    def is_published(self):
        """检查文章是否已发布"""
        return self.status == 'published'


class SocialLink(models.Model):
    """社交链接"""
    PLATFORM_CHOICES = (
        ('github', 'GitHub'),
        ('bilibili', 'Bilibili'),
        ('xiaohongshu', '小红书'),
        ('twitter', 'Twitter'),
        ('weibo', '微博'),
    )

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name="平台")
    url = models.URLField(verbose_name="链接地址")
    icon_class = models.CharField(max_length=50, blank=True, verbose_name="图标CSS类")
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name="显示顺序")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")

    class Meta:
        verbose_name = "社交链接"
        verbose_name_plural = "社交链接"
        ordering = ['display_order']

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"


class SiteStat(models.Model):
    """网站统计"""
    key = models.CharField(max_length=50, unique=True, verbose_name="统计键")
    value = models.IntegerField(default=0, verbose_name="统计值")
    description = models.CharField(max_length=200, blank=True, verbose_name="描述")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "网站统计"
        verbose_name_plural = "网站统计"

    def __str__(self):
        return f"{self.key}: {self.value}"

    @classmethod
    def get_value(cls, key, default=0):
        """获取统计值"""
        stat, created = cls.objects.get_or_create(key=key, defaults={'value': default})
        return stat.value

    @classmethod
    def increment(cls, key, amount=1):
        """增加统计值"""
        stat, created = cls.objects.get_or_create(key=key, defaults={'value': 0})
        stat.value += amount
        stat.save()
        return stat.value
