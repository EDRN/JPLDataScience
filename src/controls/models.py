# encoding: utf-8

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class AnalyticsSnippet(models.Model):
    '''JavaScript support for website analytics.'''
    LOCATIONS = [('h', 'Header'), ('b', 'Bottom')]
    location = models.CharField(
        max_length=1, choices=LOCATIONS, default='b', blank=False, null=False,
        help_text='Where to inject this; in the <head> or at the bottom before the closing </body>'
    )
    code = models.TextField(
        blank=False, null=False, default='<script></script>', help_text='JavaScript analytics code'
    )
    panels = [FieldPanel('location'), FieldPanel('code')]
    def __str__(self):
        return self.code
