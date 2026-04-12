#!/usr/bin/env python
"""
博客网站初始化脚本
用于创建超级用户、示例分类、文章和社交链接
"""

import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article, Category, SocialLink, SiteStat


def create_superuser():
    """创建超级用户"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f'✅ 已创建超级用户: {username} / {password}')
    else:
        print(f'⚠️ 超级用户已存在: {username}')


def create_categories():
    """创建示例分类"""
    categories = [
        {'name': '技术教程', 'slug': 'tutorial', 'description': '编程和技术教程'},
        {'name': '生活随笔', 'slug': 'life', 'description': '生活感悟和随笔'},
        {'name': '读书笔记', 'slug': 'reading', 'description': '读书心得和笔记'},
        {'name': '项目分享', 'slug': 'project', 'description': '项目经验和分享'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f'✅ 已创建分类: {cat_data["name"]}')
        else:
            print(f'⚠️ 分类已存在: {cat_data["name"]}')


def create_articles():
    """创建示例文章"""
    # 获取第一个分类和超级用户
    category = Category.objects.first()
    author = User.objects.filter(is_superuser=True).first()
    
    if not category or not author:
        print('⚠️ 需要先创建分类和用户')
        return
    
    articles = [
        {
            'title': '欢迎来到我的博客',
            'slug': 'welcome-to-my-blog',
            'content': '''
# 欢迎来到我的博客！

这是我的第一篇博客文章，用于测试博客系统功能。

## 功能特性

1. **Markdown 支持**：文章使用 Markdown 格式编写
2. **响应式设计**：适配手机、平板和桌面
3. **随机推荐**：侧边栏会随机推荐文章
4. **日历功能**：显示有文章的日期

## 代码示例

```python
def hello_world():
    print("Hello, World!")
    return "Welcome to my blog!"
```

> 欢迎关注我的社交媒体，获取更多更新！
            ''',
            'excerpt': '这是我的第一篇博客文章，介绍网站的功能和特性。',
            'status': 'published',
            'views': 42,
            'likes': 15,
        },
        {
            'title': 'Django 博客开发指南',
            'slug': 'django-blog-guide',
            'content': '''
# Django 博客开发指南

本文将介绍如何使用 Django 开发一个功能完整的博客系统。

## 核心功能

1. **文章管理系统**：支持 Markdown 编辑和渲染
2. **用户权限控制**：管理员可发布文章，访客可浏览
3. **API 接口**：提供日历数据和随机文章接口
4. **前端交互**：使用原生 JavaScript 实现动态功能

## 技术栈

- Django 4.2
- SQLite (开发环境)
- django-markdownx
- 原生 HTML/CSS/JavaScript

## 部署建议

建议使用以下方式部署：

1. 使用 PostgreSQL 作为生产数据库
2. 使用 Gunicorn + Nginx 部署
3. 配置 SSL 证书
4. 使用 CDN 加速静态文件

            ''',
            'excerpt': '学习如何使用 Django 构建一个完整的博客系统。',
            'status': 'published',
            'views': 89,
            'likes': 32,
        },
        {
            'title': '前端日历组件实现',
            'slug': 'frontend-calendar-component',
            'content': '''
# 前端日历组件实现

本文将介绍如何使用原生 JavaScript 实现一个交互式日历组件。

## 功能需求

1. 显示当前月份
2. 高亮有文章的日期
3. 支持月份切换
4. 点击日期可查看相关文章

## 实现思路

```javascript
function renderCalendar(year, month) {
    // 计算月份的第一天和最后一天
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    // 生成日历网格
    // ...
}
```

## 注意事项

- 需要考虑时区问题
- 移动端适配
- 性能优化

            ''',
            'excerpt': '使用原生 JavaScript 实现交互式日历组件。',
            'status': 'published',
            'views': 56,
            'likes': 21,
        },
    ]
    
    for i, article_data in enumerate(articles):
        # 设置发布时间（每篇文章间隔一天）
        published_at = timezone.now() - timedelta(days=len(articles) - i)
        
        article, created = Article.objects.get_or_create(
            slug=article_data['slug'],
            defaults={
                'title': article_data['title'],
                'author': author,
                'category': category,
                'content': article_data['content'],
                'excerpt': article_data['excerpt'],
                'status': article_data['status'],
                'views': article_data['views'],
                'likes': article_data['likes'],
                'published_at': published_at,
            }
        )
        
        if created:
            print(f'✅ 已创建文章: {article_data["title"]}')
        else:
            print(f'⚠️ 文章已存在: {article_data["title"]}')


def create_social_links():
    """创建社交链接"""
    social_links = [
        {
            'platform': 'github',
            'url': 'https://github.com/lvy-neko',
            'icon_class': 'fab fa-github',
            'display_order': 1,
        },
        {
            'platform': 'bilibili',
            'url': 'https://space.bilibili.com/123456',
            'icon_class': 'fab fa-bilibili',
            'display_order': 2,
        },
        {
            'platform': 'xiaohongshu',
            'url': 'https://www.xiaohongshu.com/user/profile/123456',
            'icon_class': 'fas fa-book',
            'display_order': 3,
        },
    ]
    
    for link_data in social_links:
        link, created = SocialLink.objects.get_or_create(
            platform=link_data['platform'],
            defaults=link_data
        )
        if created:
            print(f'✅ 已创建社交链接: {link_data["platform"]}')
        else:
            print(f'⚠️ 社交链接已存在: {link_data["platform"]}')


def create_site_stats():
    """创建网站统计"""
    # 更新文章总数
    article_count = Article.objects.filter(status='published').count()
    SiteStat.increment('article_count', article_count)
    print(f'✅ 已更新文章总数: {article_count}')
    
    # 创建其他统计
    stats = [
        {'key': 'total_views', 'value': 0, 'description': '总访问量'},
        {'key': 'total_likes', 'value': 0, 'description': '总点赞数'},
    ]
    
    for stat_data in stats:
        stat, created = SiteStat.objects.get_or_create(
            key=stat_data['key'],
            defaults=stat_data
        )
        if created:
            print(f'✅ 已创建统计: {stat_data["key"]}')
        else:
            print(f'⚠️ 统计已存在: {stat_data["key"]}')


def main():
    """主函数"""
    print('=' * 50)
    print('博客网站数据初始化')
    print('=' * 50)
    
    create_superuser()
    create_categories()
    create_articles()
    create_social_links()
    create_site_stats()
    
    print('=' * 50)
    print('✅ 初始化完成！')
    print('=' * 50)
    print('访问信息:')
    print('- 后台地址: http://127.0.0.1:8000/admin/')
    print('- 用户名: admin')
    print('- 密码: admin123')
    print('- 前台地址: http://127.0.0.1:8000/')
    print('=' * 50)


if __name__ == '__main__':
    main()