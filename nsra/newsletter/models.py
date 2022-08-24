from django.db import models
from birdsong.models import Campaign
from nsra.base.blocks import BaseStreamBlock
from birdsong.blocks import DefaultBlocks
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel 
from wagtail.core.fields import StreamField

class Newsletter(Campaign):

    headline = models.CharField(
        max_length=255,
        help_text="The headline to use for the newsletter.",
        null=True, blank=True,
    )

    header_background = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        help_text="The image to use for the header backgound.",
        on_delete=models.SET_NULL,
    )

    body = StreamField(
        DefaultBlocks(), 
        verbose_name="email body content block",
        blank = False,
        null=True
    )

    panels = Campaign.panels + [
        FieldPanel("headline"),
        ImageChooserPanel("header_background"),
        StreamFieldPanel("body"),
    ]