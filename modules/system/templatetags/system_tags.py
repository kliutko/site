from django import template
from django.db.models import Count
from taggit.models import Tag
from datetime import datetime, date, time, timedelta
from django.db.models import Count, Q
from django.utils import timezone

from ..models import About, Faq

register = template.Library()


@register.simple_tag
def tag_about():
    about = About.objects.filter(id=1)
    return about

# @register.simple_tag
# def tag_faq():
#     about = Faq.objects.all()
#     return about
