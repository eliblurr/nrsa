
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock, URLBlock, PageChooserBlock
)


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
    ], blank=True, required=False)

    color = ChoiceBlock(choices=[
        ('', 'Select a header color'),
        ('#EB3438', 'red'),
        ('#F4E726', 'yellow'),
        ('#009933', 'green'),
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"

class LinkBlock(StructBlock):
    title = CharBlock(classname="title", required=True)
    link = URLBlock(blank=False, required=True,)

    class Meta:
        icon = "link"
        template = "blocks/linkblock.html"

class CTABlock(StructBlock):
    """
        Custom `StructBlock` that allows CTA actions
    """
    cta_title = CharBlock(classname="title", required=True)
    page = PageChooserBlock(label="page", required=True)
    
    class Meta:
        icon = "login"
        template = "blocks/ctablock.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="form",
        template="blocks/paragraph_block.html"
    )
    link_block = LinkBlock()
    cta_block = CTABlock()
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="link-external",
        template="blocks/embed_block.html")

class ParagraphStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="form",
        template="blocks/paragraph_block.html"
    )
    link_block = LinkBlock()
    cta_block = CTABlock()
    block_quote = BlockQuote()
