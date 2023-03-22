# encoding: utf-8

'''📀🔬 Data Science: models.'''


from django.db import models
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel


@register_setting
class Footer(BaseSiteSetting):
    '''Settings for the footer.'''
    site_manager = models.CharField(null=False, blank=True, max_length=60, help_text='Name of the site manager')
    webmaster = models.CharField(null=False, blank=True, max_length=60, help_text='Name of the webmaster')
    clearance = models.CharField(null=False, blank=True, max_length=20, help_text='Clearance №')
    panels = [FieldPanel('site_manager'), FieldPanel('webmaster'), FieldPanel('clearance')]

