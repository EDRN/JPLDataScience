# encoding: utf-8

'''📀🔬 Blocks.'''

from django.utils.html import format_html
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock as BaseTableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock as BaseTypedTableBlock
from wagtail.images.blocks import ImageChooserBlock


class TitleBlock(blocks.StructBlock):
    '''A large title.'''
    text = blocks.CharBlock(max_length=100, required=True, help_text='Title to display')
    class Meta:
        template = 'edrnsite.streams/title-block.html'
        icon = 'title'
        label = 'Title'
        help_text = 'Large title text to display on the page'


class TableBlock(BaseTableBlock):
    '''A basic table to appear in the EDRN site.'''
    class Meta(object):
        template = 'edrnsite.streams/table-block.html'
        icon = 'table'
        label = 'Basic (Plain Text) Table'


class TypedTableBlock(BaseTypedTableBlock):
    '''A more advanced table to appear in the EDRN site.'''
    class Meta(object):
        template = 'edrnsite.streams/typed-table-block.html'
        icon = 'table'
        label = 'Advanced Table'


class BlockQuoteBlock(blocks.BlockQuoteBlock):
    '''Override Wagtail's own BlockQuoteBlock so we can use Bootstrap styling.'''
    def render_basic(self, value, context=None):
        if value:
            return format_html('<blockquote class="blockquote">{0}</blockquote>', value)
        else:
            return ''


TYPED_TABLE_BLOCK = TypedTableBlock([
    ('text', blocks.CharBlock(help_text='Plain text cell')),
    ('rich_text', blocks.RichTextBlock(help_text='Rich text cell')),
    ('numeric', blocks.FloatBlock(help_text='Numeric cell')),
    ('integer', blocks.IntegerBlock(help_text='Integer cell')),
    ('page', blocks.PageChooserBlock(help_text='Page within the site')),
])


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    label = blocks.CharBlock(max_length=120, required=False, help_text='Overlaid label, if any')
    caption = blocks.CharBlock(max_length=400, required=False, help_text='Overlaid caption, if any')
    class Meta:
        icon = 'placeholder'
        label = 'Captioned Image'
        help_text = 'An image with both a shorter label and a longer caption'
