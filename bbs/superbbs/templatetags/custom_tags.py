from django import template
from django.utils.html import format_html

register=template.Library()

@register.filter
def truncate_img_url(url):
    return "/".join(url.name.split("/")[1:])

@register.simple_tag
def comment_count(article_obj):
    query_set=article_obj.comment_set.select_related()
    counts={
        'comment_count':query_set.filter(comment_type=1).count(),
        'thumb_count':query_set.filter(comment_type=2).count(),
    }
    return counts