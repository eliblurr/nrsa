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
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from nsra.news_and_events.models import NewsPage
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

class HomePageCoreFunctionOrderable(Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='functions')
    function = models.ForeignKey('core_functions.CoreFunction', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('function'),
    ]

class HomePageActivitiesOrderable(Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='activities')
    activity = models.ForeignKey('activity.ActivityPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('activity'),
    ]

class HomePagePublicationAndResearch(Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='publication_and_research')
    publications = models.ForeignKey('research_and_publication.PublicationPage', null=True, blank=True, on_delete=models.CASCADE)
    research = models.ForeignKey('research_and_publication.ResearchPage', null=True, blank=True, on_delete=models.CASCADE)

    @property
    def selection(self):
        if self.research:
            return self.research
        return self.publications

    def clean(self):
        data = self
        if (self.publications and self.research) or (not self.publications and not self.research):
            raise forms.ValidationError('only one page selection is allowed')
        return self
    
    panels = [
        PageChooserPanel('publications'),
        PageChooserPanel('research'),
    ]

class SectionLinkOrderable(Orderable):

    section = ParentalKey(
        'home.HomePageSectionOrderable',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='pages',
    )

    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='select section page',
        verbose_name='Section Page'
    )

    panels = [
        # PageChooserPanel(
        #     'page',
        #     [
        #         'research_and_publication.PublicationPage',
        #         'research_and_publication.ResearchPage',
        #         'news_and_events.NewsPage',
        #         'news_and_events.EventPage',
        #         'activity.ActivityPage',
        #         'galleries.GalleryPage',
        #     ], can_choose_root=False
        # )
        FieldPanel('section')
    ]

class HomePageSectionOrderable(ClusterableModel, Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='sections')
    section_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the featured section'
    )

    section_description = models.TextField(
        null=True,
        blank=True,
        help_text='Description to display above the featured section'
    )
    
    section_cta = models.CharField(
        verbose_name='Section CTA',
        max_length=255,
        null=True,
        blank=True,
        help_text='Text to display on Call to Action'
    )

    section_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Section CTA link',
        help_text='Choose a page to link to for the Call to Action(normally some index page)'
    )

    section_color = models.CharField(
        max_length=10,
        choices=COLORS,
        null=True,
        blank=True,
        verbose_name="section backgroung color"
    )

    panels = [
        
        FieldPanel('section_title'),
        FieldPanel('section_description'),
        FieldPanel('section_cta'),
        PageChooserPanel('section_cta_link'),
        FieldPanel('section_color'),
        # PageChooserPanel(
        #     "pages____page"
        # ),
        InlinePanel(
            'pages',
            label='Section pages',
        #     panels=[
        # #     #     PageChooserPanel(
        # #     #         "pages"
        # #     #         , [], can_choose_root=False
        # #     #     )
        #     # ],
        ),
    ]
  
class HomePage(StandardPage):

    templates = "home/home_page.html"
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

    # statistics
    statistics_title = models.CharField(max_length=1000, null=True, blank=True, verbose_name='title',)
    statistics_sub_title = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Subtitle',)
    statistics_description = models.TextField(null=True, blank=True, verbose_name='Description',)
    statistics_image = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Statistics image',
        help_text='Choose an image to show alongside statistics text'
    )
    statistics_cta_text = models.CharField(max_length=1000, null=True, blank=True, verbose_name='CTA text',)
    statistics_cta_link = models.ForeignKey(
        'stats.StatisticsIndexPage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Statistics CTA link',
        help_text='Choose a statistics page to link to for the Call to Action(normally some index page)'
    )

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

    statistics_panels = [
        MultiFieldPanel([
            FieldPanel('statistics_title'),
            FieldPanel('statistics_sub_title'),
            FieldPanel('statistics_description'),
            ImageChooserPanel('statistics_image'),
            FieldPanel('statistics_cta_text'),
            PageChooserPanel('statistics_cta_link'),
        ]),
    ]

    section_panels = [
        InlinePanel(
            'sections', min_num=0,
        ),
    ]

    core_function_panel = [
        MultiFieldPanel([
            FieldPanel('functions_title'),
            FieldPanel('functions_sub_title'),
            FieldPanel('functions_description'),
            FieldPanel('functions_cta_text'),
            FieldPanel('functions_cta_link'),
        ]),
        InlinePanel('functions', min_num=0),
    ]

    activity_panel = [
        InlinePanel('activities', min_num=0),
    ]

    publication_and_research_panel = [
        InlinePanel('publication_and_research', min_num=0),
    ]


    edit_handler = TabbedInterface([
        ObjectList(standard_page_content_panels, heading='page & hero'),
        ObjectList(content_panels, heading='body'),         
        ObjectList(core_function_panel, heading='core functions'), 
        ObjectList(activity_panel, heading='press briefings'), 
        ObjectList(publication_and_research_panel, heading='publications and research'), 
        ObjectList(section_panels, heading='sections'), 
        ObjectList(statistics_panels, heading='statistics'), 
        ObjectList(StandardPage.promote_panels, heading='promote'),
        ObjectList(StandardPage.settings_panels, heading='settings'),
    ])

    # get news for the past week for the past week
    def get_latest_news(self):
        today = datetime.date.today()
        a_week_ago = today - datetime.timedelta(days=7)
        return NewsPage.objects.filter().live().descendant_of(self).order_by('-first_published_at')[:16]

    # get latest acticities
    # get latest press briefings
    # get publication and research
    # core functions

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        latest_news = self.paginate(request, self.get_latest_news, size=4)

        # page = [page for page in latest_news.paginator][1]

        # print(dir(latest_news), latest_news.count, sep='\n')
        context['latest_news'] = latest_news
        return context
