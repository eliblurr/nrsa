from django.db import models
from wagtail.search import index
from nsra.base.validators import phone_validator
from wagtail.core.models import Page, Orderable
from django.core.exceptions import ValidationError
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm, AbstractForm
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from nsra.news_and_events.models import NewsEventsIndexPage
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from wagtail.core.blocks import StreamBlock
from modelcluster.fields import ParentalKey
from nsra.base.blocks import BaseStreamBlock
from nsra.base.models import StandardPage
from nsra.base.choices import COLORS
from django import forms
import datetime
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
    PageChooserPanel,
    MultiFieldPanel,
    FieldRowPanel,
    InlinePanel,
    FieldPanel,
)

from nsra.regional_profiles.models import RegionalProfilePage

class AboutUsPageCoreFunctionOrderable(Orderable):
    page = ParentalKey('about_us.AboutUsPage', on_delete=models.CASCADE, related_name='functions')
    function = models.ForeignKey('core_functions.CoreFunction', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('function'),
    ]


class AboutUsPageCarouselImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("about_us.AboutUsPage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [ImageChooserPanel("carousel_image")]

class ExecutiveOrderable(Orderable):
    page = ParentalKey('about_us.AboutUsPage', on_delete=models.CASCADE, related_name='executives')
    executive = models.ForeignKey('executive.Executive', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('executive'),
    ]

class RelatedOrganizationOrderable(Orderable):
    page = ParentalKey('about_us.AboutUsPage', on_delete=models.CASCADE, related_name='related_organizations')
    organization = models.ForeignKey('base.RelatedOrganization', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('organization'),
    ]

# REGIONAL PROFILES
  
class AboutUsPage(StandardPage):
    
    templates = "about_us/about_us_page.html"
    max_count = 1

    body = StreamField(
        [
            ('base', BaseStreamBlock()), # each block is stacked in template 
            ('grid', StreamBlock( # each block is arranged in 2 grid system
                [ 
                    ('paragraph', ParagraphStreamBlock()), # each block is stacked in template 
                    ('image', ImageBlock()),
                ]
            ))
        ],
        null=True,
        blank=True
    )

    executive_panels = [
        InlinePanel('executives', min_num=0),
    ]

    organization_panels = [
        InlinePanel('related_organizations', min_num=0),
    ]

    # mission
    # add validation here for when there is title description required
    mission_title = models.CharField( 
        max_length=1000,
        verbose_name='Section CTA link',
        help_text='mission title here',
        default='MISSION'
    )
    mission_sub_title = models.CharField(
        max_length=1000,
        verbose_name='mission sub title',
        help_text='mission subtitle here', null=True, blank=True
    )
    mission_description = models.TextField(null=True, blank=True)
    mission_icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    # vision

    vision_title = models.CharField(
        max_length=1000,
        verbose_name='vision title',
        help_text='vision title here',
        default='VISION'
    )
    vision_sub_title = models.CharField(
        max_length=1000,
        verbose_name='vision subtitle',
        help_text='vision subtitle here', null=True, blank=True
    )
    vision_description = models.TextField(null=True, blank=True)
    vision_icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    # mandate

    mandate_title = models.CharField(
        max_length=1000,
        verbose_name='mandate title',
        help_text='mandate title here',
        default='MANDATE'
    )
    mandate_sub_title = models.CharField(
        max_length=1000,
        verbose_name='mandate subtitle',
        help_text='mandate subtitle here', null=True, blank=True
    )
    mandate_description = models.TextField(null=True, blank=True)
    mandate_icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    

    # core functions
    functions_title = models.CharField(max_length=1000, null=True, blank=True, verbose_name='title',)
    functions_sub_title = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Subtitle',)
    functions_description = models.TextField(null=True, blank=True, verbose_name='Description',)
    functions_cta_text = models.CharField(max_length=1000, null=True, blank=True, verbose_name='CTA text',)
    functions_cta_link = models.ForeignKey(
        'core_functions.CoreFunctionIndexPage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Core Function Index CTA link',
        help_text='Choose a core function index page to link to for the Call to Action(normally some index page)'
    )

    search_fields = StandardPage.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
    ]

    standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

    content_panels =  [
        StreamFieldPanel('body'),
    ]

    core_function_panel = [
        MultiFieldPanel([
            FieldPanel('functions_title'),
            FieldPanel('functions_sub_title'),
            FieldPanel('functions_description'),
            FieldPanel('functions_cta_text'),
            FieldPanel('functions_cta_link'),
        ]),
        InlinePanel('functions', min_num=1),
    ]

    mvm_panels = [
        MultiFieldPanel([
            FieldPanel('mission_title'),
            FieldPanel('mission_sub_title'),
            FieldPanel('mission_description'),
            FieldPanel('mission_icon'),
        ], heading="mission"),

        MultiFieldPanel([
            FieldPanel('vision_title'),
            FieldPanel('vision_sub_title'),
            FieldPanel('vision_description'),
            FieldPanel('vision_icon'),
        ], heading="vision"),

        MultiFieldPanel([
            FieldPanel('mandate_title'),
            FieldPanel('mandate_sub_title'),
            FieldPanel('mandate_description'),
            FieldPanel('mandate_icon'),
        ], heading="mandate"),
    ]

    carousel_panel = [
        MultiFieldPanel(
            [InlinePanel("carousel_images", min_num=0, label="Image")],
            heading="Carousel Images",
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(standard_page_content_panels, heading='page & hero'),
        ObjectList(carousel_panel, heading='carousel images'),
        ObjectList(content_panels, heading='body'),         
        ObjectList(core_function_panel, heading='core functions'), 
        ObjectList(executive_panels, heading='Executives'), 
        ObjectList(organization_panels, heading='Related Organizations'), 
        ObjectList(mvm_panels, heading='mvm'), 
        ObjectList(StandardPage.promote_panels, heading='promote'),
        ObjectList(StandardPage.settings_panels, heading='settings'),
    ])

    def get_executives(self):
        return self.executives.filter(executive__featured=True).all()

    def get_related_organizations(self):
        return self.related_organizations.filter(organization__featured=True).all()
    
    def get_context(self, request):
        context = super(AboutUsPage, self).get_context(request)
        context['executives'] = self.get_executives()
        context['related_organizations'] = self.get_related_organizations()
        context['regional_profiles'] = self.get_children().type(RegionalProfilePage).live()
        return context