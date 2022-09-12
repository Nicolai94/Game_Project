from django import template
from main.models import News


register = template.Library()


@register.inclusion_tag('inc/latest_news.html')
def get_last_news(count=5):
    last_news = News.objects.all()[:count]
    return {'last_news': last_news}