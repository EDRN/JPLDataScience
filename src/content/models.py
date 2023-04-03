# encoding: utf-8

'''📀🔬 Data Science: content models.'''


from blocks import blocks
from django.db import models
from django.http import HttpRequest
from wagtail import blocks as wagtail_core_blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail_blocks.blocks import HeaderBlock, ImageTextOverlayBlock, ListWithImagesBlock, ThumbnailGalleryBlock


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
        ('rich_text', wagtail_core_blocks.RichTextBlock(
            label='Rich Text', icon='doc-full', help_text='Richly formatted text'
        )),
        ('title', blocks.TitleBlock()),
        ('header', HeaderBlock()),
        ('table', blocks.TableBlock()),
        ('typed_table', blocks.TYPED_TABLE_BLOCK),
        ('block_quote', blocks.BlockQuoteBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('list_with_images', ListWithImagesBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
        ('raw_html', wagtail_core_blocks.RawHTMLBlock(help_text='Raw HTML (use with care)')),
    ], null=True, blank=True, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel('body')]
    search_fields = Page.search_fields + [index.SearchField('body')]


class NewsItem(Page):
    template = 'content/news-item.html'
    page_description = 'An item of newsworthiness'
    release_date = models.DateField(null=False, blank=False, help_text="Date of this news item's release")
    lead_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='news_item_lead_image',
        help_text='Lead image'
    )
    caption = models.CharField(null=False, blank=True, help_text='Optional caption for the lead image', max_length=2000)
    body = StreamField([
        ('rich_text', wagtail_core_blocks.RichTextBlock(
            label='Rich Text', icon='doc-full', help_text='Richly formatted text'
        )),
        ('title', blocks.TitleBlock()),
        ('header', HeaderBlock()),
        ('block_quote', blocks.BlockQuoteBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('list_with_images', ListWithImagesBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
        ('raw_html', wagtail_core_blocks.RawHTMLBlock(help_text='Raw HTML (use with care)')),
    ], null=True, blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel('release_date'), FieldPanel('lead_image'), FieldPanel('caption'), FieldPanel('body')
    ]
    search_fields = Page.search_fields + [index.SearchField('body'), index.SearchField('caption')]


class NewsIndex(Page):
    template = 'content/news-index.html'
    page_description = 'A container for news items'
    subpage_types = [NewsItem]
    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        context = super().get_context(request, *args, **kwargs)
        news_items = NewsItem.objects.child_of(self).live().public().order_by('-release_date')
        context['news_item_count'] = news_items.count()
        context['news_items'] = news_items
        return context
