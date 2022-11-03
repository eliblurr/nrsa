from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from nsra.base.models import GalleryImageBase, StandardPage
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.blocks import CharBlock
from nsra.base.models import BaseModel
from wagtail.core.models import Page
from wagtail.search import index
from django.db import models
from django import forms

standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

class Regions(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    panels = [FieldPanel('name')]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Regions'

from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from wagtail.core.blocks import StreamBlock
from nsra.base.blocks import BaseStreamBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

class RegionalProfilePage(StandardPage):

    templates = "regional_profiles/regional_profile_page.html"

    headline = models.CharField(blank=False, null=False, max_length=250)
    description = models.CharField(blank=True, null=True, max_length=5000)
    region = models.OneToOneField('Regions', on_delete=models.PROTECT, related_name='+')

    map_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    director_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # map_data

    address = StreamField(
        [
            ('address_line', CharBlock(
                icon="form",
                template="blocks/address_line.html"
            )), 
        ],
        null=True,
        blank=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('headline'),
        index.SearchField('body'),
        index.SearchField('region'),
    ]

    content_panels = [
        MultiFieldPanel([
            FieldPanel('headline'),
            FieldPanel('description'),
            FieldPanel('region'),
            ImageChooserPanel('map_image'),
            ImageChooserPanel('director_image'),
        ], heading="content"),
    ]

    map_data_panels = [
        MultiFieldPanel([
            StreamFieldPanel('address'),
        ], heading="map data"),
    ]

    page_links = [
        TabbedInterface([
            InlinePanel('activities', heading='Activity links'),
            InlinePanel('events', heading='Event links'),
            InlinePanel('news', heading='News links'),
        ]),     
    ]

    edit_handler = TabbedInterface([
        ObjectList(standard_page_content_panels, heading='page & hero'),
        ObjectList(content_panels, heading='content'), 
        ObjectList([FieldPanel('body', heading='body')], heading='body'), 
        ObjectList(map_data_panels, heading='map data'),
        ObjectList(page_links, heading='page links'),
        ObjectList(StandardPage.promote_panels, heading='promote'),
        ObjectList(StandardPage.settings_panels, heading='settings'),
    ])

    def get_context(self, request):
        return super(RegionalProfilePage, self).get_context(request)
    
    class Meta:
        verbose_name = 'Regional Profile'
        verbose_name_plural = 'Regional Profiles'


class ActivityOrderable(Orderable):
    page = ParentalKey('regional_profiles.RegionalProfilePage', on_delete=models.CASCADE, related_name='activities')
    activity = models.ForeignKey('activity.ActivityPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('activity'),
    ]

class NewsOrderable(Orderable):
    page = ParentalKey('regional_profiles.RegionalProfilePage', on_delete=models.CASCADE, related_name='news')
    news = models.ForeignKey('news_and_events.NewsPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('news'),
    ]

class EventOrderable(Orderable):
    page = ParentalKey('regional_profiles.RegionalProfilePage', on_delete=models.CASCADE, related_name='events')
    event = models.ForeignKey('news_and_events.EventPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('event'),
    ]
