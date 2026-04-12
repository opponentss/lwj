from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from django.views.decorators.http import require_GET
import random
from datetime import datetime, timedelta

from .models import Article, Category, SocialLink, SiteStat


def home(request):
    """首页视图"""
    # 获取已发布的最新文章
    articles = Article.objects.filter(status='published').order_by('-published_at')[:10]
    
    # 获取社交链接
    social_links = SocialLink.objects.filter(is_active=True).order_by('display_order')
    
    # 获取文章总数统计
    article_count = SiteStat.get_value('article_count', Article.objects.filter(status='published').count())
    
    # 获取当前月份有文章的日期
    today = timezone.now()
    current_month = today.month
    current_year = today.year
    
    # 获取本月有文章的日期列表
    article_dates = Article.objects.filter(
        status='published',
        published_at__year=current_year,
        published_at__month=current_month
    ).dates('published_at', 'day')
    
    context = {
        'articles': articles,
        'social_links': social_links,
        'article_count': article_count,
        'current_year': current_year,
        'current_month': current_month,
        'article_dates': [d.day for d in article_dates],
        'today': today,
    }
    return render(request, 'blog/index.html', context)


def article_detail(request, slug):
    """文章详情页"""
    article = get_object_or_404(Article, slug=slug, status='published')
    
    # 增加阅读量
    article.increase_views()
    
    # 获取随机推荐文章（排除当前文章）
    all_articles = Article.objects.filter(status='published').exclude(id=article.id)
    if all_articles.count() >= 2:
        random_articles = random.sample(list(all_articles), 2)
    elif all_articles.exists():
        random_articles = list(all_articles)
    else:
        random_articles = []
    
    # 获取社交链接
    social_links = SocialLink.objects.filter(is_active=True).order_by('display_order')
    
    context = {
        'article': article,
        'random_articles': random_articles,
        'social_links': social_links,
    }
    return render(request, 'blog/article_detail.html', context)


def about(request):
    """关于页面"""
    social_links = SocialLink.objects.filter(is_active=True).order_by('display_order')
    context = {
        'social_links': social_links,
    }
    return render(request, 'blog/about.html', context)


@require_GET
def random_articles_api(request):
    """随机文章API，用于侧边栏随机推荐"""
    count = int(request.GET.get('count', 2))
    exclude_id = request.GET.get('exclude', None)
    
    articles = Article.objects.filter(status='published')
    if exclude_id:
        articles = articles.exclude(id=exclude_id)
    
    if articles.count() <= count:
        random_articles = list(articles)
    else:
        random_articles = random.sample(list(articles), count)
    
    data = [
        {
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            'excerpt': article.excerpt[:100] if article.excerpt else article.content[:100],
            'published_at': article.published_at.strftime('%Y-%m-%d'),
            'views': article.views,
            'likes': article.likes,
        }
        for article in random_articles
    ]
    
    return JsonResponse({'articles': data})


@require_GET
def calendar_data_api(request):
    """日历数据API，返回指定月份有文章的日期"""
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    article_dates = Article.objects.filter(
        status='published',
        published_at__year=year,
        published_at__month=month
    ).dates('published_at', 'day')
    
    dates = [d.day for d in article_dates]
    
    return JsonResponse({
        'year': year,
        'month': month,
        'dates': dates,
    })


@require_GET
def article_list_api(request):
    """文章列表API，用于分页加载"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    
    articles = Article.objects.filter(status='published').order_by('-published_at')
    paginator = Paginator(articles, per_page)
    
    try:
        page_obj = paginator.page(page)
    except:
        page_obj = paginator.page(1)
    
    data = [
        {
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            'excerpt': article.excerpt[:150] if article.excerpt else article.content[:150],
            'published_at': article.published_at.strftime('%Y-%m-%d'),
            'views': article.views,
            'likes': article.likes,
            'category': article.category.name if article.category else None,
        }
        for article in page_obj
    ]
    
    return JsonResponse({
        'articles': data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
    })
