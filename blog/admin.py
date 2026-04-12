from django.contrib import admin
from django.utils.html import format_html
from markdownx.admin import MarkdownxModelAdmin
from .models import Article, Category, SocialLink, SiteStat


class ArticleAdmin(MarkdownxModelAdmin):
    """文章管理界面配置"""
    list_display = ('title', 'author', 'category', 'status', 'published_at', 'views', 'likes')
    list_filter = ('status', 'category', 'published_at', 'author')
    search_fields = ('title', 'content', 'excerpt')
    readonly_fields = ('views', 'likes', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('内容', {
            'fields': ('content', 'excerpt', 'cover_image')
        }),
        ('统计信息', {
            'fields': ('views', 'likes'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """保存模型时设置作者"""
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    """分类管理界面"""
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class SocialLinkAdmin(admin.ModelAdmin):
    """社交链接管理界面"""
    list_display = ('platform', 'url', 'display_order', 'is_active')
    list_filter = ('platform', 'is_active')
    list_editable = ('display_order', 'is_active')
    ordering = ('display_order',)


class SiteStatAdmin(admin.ModelAdmin):
    """网站统计管理界面"""
    list_display = ('key', 'value', 'description', 'updated_at')
    readonly_fields = ('updated_at',)
    search_fields = ('key', 'description')


# 注册模型到管理后台
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(SiteStat, SiteStatAdmin)

# 自定义管理后台标题
admin.site.site_header = '博客管理后台'
admin.site.site_title = '博客管理'
admin.site.index_title = '网站管理'
