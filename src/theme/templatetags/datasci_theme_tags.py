# encoding: utf-8

'''📀🔬 Data Science theme: Django template tags.'''

from ..models import Footer
from django import template
from django.template.context import Context
from wagtail.models import Site
from wagtailmenus.models import FlatMenu
from wagtailmenus.templatetags.menu_tags import flat_menu


register = template.Library()


@register.inclusion_tag('theme/menus/footer-menus.html', takes_context=True)
def datasci_footer_menus(context: Context) -> dict:
    menus = FlatMenu.objects.filter(handle__startswith='footer-').order_by('title')
    return {'menus': menus, 'original_context': context}


@register.simple_tag(takes_context=True)
def request_restoring_flat_menu(context: Context, original_context: Context, **kwargs):
    context['request'] = original_context['request']
    rc = flat_menu(context, **kwargs)
    return rc


@register.inclusion_tag('theme/colophon-byline.html', takes_context=False)
def jpl_colophon_byline() -> dict:
    byline, footer = {}, Footer.for_site(Site.objects.filter(is_default_site=True).first())
    byline['manager'] = footer.site_manager if footer.site_manager else 'unknown'
    byline['webmaster'] = footer.webmaster if footer.webmaster else 'unknown'
    byline['clearance'] = footer.clearance if footer.clearance else 'unknown'
    return byline
