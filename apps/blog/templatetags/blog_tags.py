from django import template
from blog.models import Blog

register = template.Library()


@register.simple_tag
def recommends():
    return Blog.get_topped_blogs()


@register.simple_tag
def latest_blogs():
    return Blog.get_latest_blogs()
