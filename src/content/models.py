# encoding: utf-8

'''📀🔬 Data Science: content models.'''


from blocks import blocks
from wagtail import blocks as wagtail_core_blocks
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.search import index


class HomePage(Page):
    template = 'content/home-page.html'
    page_description = 'A content type specifically for the home page of the entire site'
    max_count = 1
    banner = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=False, on_delete=models.SET_NULL,
        help_text='Banner image that bleeds into the top of the page', related_name='+'
    )
    body = StreamField([
        ('title', blocks.TitleBlock()),
        ('rich_text', wagtail_core_blocks.RichTextBlock(
            label='Rich Text', icon='doc-full', help_text='Richly formatted text'
        )),
        ('block_quote', blocks.BlockQuoteBlock()),
        ('raw_html', wagtail_core_blocks.RawHTMLBlock(help_text='Raw HTML (use with care)'))
    ], null=True, blank=True, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel('banner'), FieldPanel('body')]
    search_fields = Page.search_fields + [index.SearchField('body')]


class FlexPage(Page):
    template = 'content/flex-page.html'
    page_description = 'A web page with flexible content'
    body = StreamField([
        ('title', blocks.TitleBlock()),
        ('rich_text', wagtail_core_blocks.RichTextBlock(
            label='Rich Text', icon='doc-full', help_text='Richly formatted text'
        )),
        ('block_quote', blocks.BlockQuoteBlock()),
        ('raw_html', wagtail_core_blocks.RawHTMLBlock(help_text='Raw HTML (use with care)'))
    ], null=True, blank=True, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel('body')]
    search_fields = Page.search_fields + [index.SearchField('body')]
