# encoding: utf-8

'''📀🔬 Data Science: content models.'''


from blocks import blocks
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail import blocks as wagtail_core_blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail_blocks.blocks import HeaderBlock, ImageTextOverlayBlock, ListWithImagesBlock, ThumbnailGalleryBlock
from wagtailcaptcha.models import WagtailCaptchaEmailForm


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


class BaseEmailForm(Page):
    '''Abstract base Wagtail model for a through-the-web form (not a Django form).'''
    subpage_types = []
    intro = RichTextField(blank=True, help_text='Introductory text to appear above the form')
    outro = RichTextField(blank=True, help_text='Text to appear below the form')
    thank_you_text = RichTextField(blank=True, help_text='Gratitude to display after form submission')
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields ✍️'),
        FieldPanel('outro'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6', help_text='From whom this email will originate'),
                FieldPanel('to_address', classname='col6', help_text='Who should receive this email; commas in between multiple addresses')
            ]),
            FieldPanel('subject')
        ], 'Email')
    ]
    class Meta:
        abstract = True


class EmailForm(BaseEmailForm, AbstractEmailForm):
    template = 'content/email-form.html'
    landing_page_template = 'content/email-form-landing.html'
    page_description = 'Form that once submitted sends an email message'


class CaptchaEmailForm(BaseEmailForm, WagtailCaptchaEmailForm):
    template = 'content/email-form.html'
    landing_page_template = 'content/email-form-landing.html'
    page_description = 'Form that once submitted sends an email message but also uses a CAPCTHA'


class LimitedFormField(AbstractFormField):
    '''This abstract form field removes the date and date/time choices.'''
    CHOICES = (
        ('singleline', _('Single line text')),
        ('multiline', _('Multi-line text')),
        ('email', _('Email')),
        ('number', _('Number')),
        ('url', _('URL')),
        ('checkbox', _('Checkbox')),
        ('checkboxes', _('Checkboxes')),
        ('dropdown', _('Drop down')),
        ('multiselect', _('Multiple select')),
        ('radio', _('Radio buttons')),
        ('hidden', _('Hidden field')),
    )
    field_type = models.CharField(verbose_name='Field Type', max_length=16, choices=CHOICES)
    class Meta:
        abstract = True
        ordering = ['sort_order']


class EmailFormField(LimitedFormField):
    page = ParentalKey(EmailForm, on_delete=models.CASCADE, related_name='form_fields')


class CaptchaEmailFormField(LimitedFormField):
    page = ParentalKey(CaptchaEmailForm, on_delete=models.CASCADE, related_name='form_fields')
