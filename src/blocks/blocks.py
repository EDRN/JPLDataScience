# encoding: utf-8

'''📀🔬 Blocks.'''

from django.utils.html import format_html
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock as BaseTableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock as BaseTypedTableBlock


class TitleBlock(blocks.StructBlock):
    '''A large title.'''
    text = blocks.CharBlock(max_length=100, required=True, help_text='Title to display')
    class Meta:
        template = 'blocks/title-block.html'
        icon = 'title'
        label = 'Title'
        help_text = 'Display-class title text'


class TableBlock(BaseTableBlock):
    '''A basic table to appear in the data science site.'''
    class Meta(object):
        template = 'blocks/table-block.html'
        icon = 'table'
        label = 'Basic Table'
        help_text = 'A table that can only contain plain text cells'


class TypedTableBlock(BaseTypedTableBlock):
    '''A more advanced table to appear in the data science site.'''
    class Meta(object):
        template = 'blocks/typed-table-block.html'
        icon = 'table'
        label = 'Advanced Table'
        help_text = 'An advanced table where each column may have a different data type'


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
