from .models import SocialLink, SiteStat, Article


def site_stats(request):
    """为所有模板提供网站统计和社交链接"""
    context = {}
    
    # 社交链接
    try:
        social_links = SocialLink.objects.filter(is_active=True).order_by('display_order')
        context['social_links'] = social_links
    except:
        context['social_links'] = []
    
    # 文章总数统计
    try:
        article_count = SiteStat.get_value('article_count', Article.objects.filter(status='published').count())
        context['article_count'] = article_count
    except:
        context['article_count'] = 0
    
    return context