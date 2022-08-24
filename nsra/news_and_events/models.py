from django.db import models
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.core.fields import RichTextField, StreamField
from nsra.base.models import GalleryImageBase, StandardPage
from wagtail.core.blocks import StreamBlock
from wagtail.search import index
from wagtail.api import APIField
from django import forms
import datetime

standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

class EventTag(TaggedItemBase):
    content_object = ParentalKey(
        'EventPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class NewsTag(TaggedItemBase):
    content_object = ParentalKey(
        'NewsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class EventPage(StandardPage):
    date_time = models.DateTimeField("Event date and time")
    headline = models.CharField(blank=True, max_length=250)
    tags = ClusterTaggableManager(through=EventTag, blank=True)

    subpage_types = []

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_related_events(self):
        return self.__class__.objects.filter(
            tags__in=self.tags.all()
        ).distinct().exclude(pk=self.pk).live().order_by('-first_published_at')

    def get_gallery(self):
        return self.gallery_images.all()

    search_fields = Page.search_fields + [
        index.SearchField('headline'),
        index.SearchField('body'),
    ]

    content_panels = [
        MultiFieldPanel([
            FieldPanel('headline'),
            FieldPanel('date_time'),
            FieldPanel('body'),
        ], heading="body"),

        MultiFieldPanel([
            FieldPanel('tags'),
        ], heading="Meta Grouping"),
    ]

    gallery_panels = [
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    edit_handler = TabbedInterface([
            ObjectList(standard_page_content_panels, heading='page & hero'),
            ObjectList(content_panels, heading='content'), 
            ObjectList(gallery_panels, heading='gallery'), 
            ObjectList(StandardPage.promote_panels, heading='promote'),
            ObjectList(StandardPage.settings_panels, heading='settings'),
        ])

    def get_context(self, request):
        context = super(EventPage, self).get_context(request)
        related_events = self.paginate(request, self.get_related_events, size=5)
        gallery_images = self.paginate(request, self.get_gallery, size=1)
        context['related_events'] = related_events
        context['gallery_images'] = gallery_images
        return context
    
    class Meta:
        verbose_name = 'Event Page'
        verbose_name_plural = 'Event Page'

class NewsPage(StandardPage):
    date = models.DateField("News date")
    headline = models.CharField(blank=True, max_length=10000)
    tags = ClusterTaggableManager(through=NewsTag, blank=True)
    # summary_title = models.CharField(blank=True, max_length=1000)
    # summary = models.CharField(blank=True, max_length=10000)

    subpage_types = []

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_related_news(self):
        return self.__class__.objects.filter(
            tags__in=self.tags.all()
        ).distinct().exclude(pk=self.pk).live().order_by('-first_published_at')

    def get_gallery(self):
        return self.gallery_images.all()

    search_fields = Page.search_fields + [
        index.SearchField('headline'),
        index.SearchField('body'),
    ]

    content_panels = [
        MultiFieldPanel([
            FieldPanel('headline'),
            FieldPanel('date'),
            FieldPanel('body'),
            # FieldPanel('summary_title'),
            # FieldPanel('summary'),
        ], heading="body"),

        MultiFieldPanel([
            FieldPanel('tags'),
        ], heading="Meta Grouping"),
    ]

    gallery_panels = [
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    edit_handler = TabbedInterface([
            ObjectList(standard_page_content_panels, heading='page & hero'),
            ObjectList(content_panels, heading='content'), 
            ObjectList(gallery_panels, heading='gallery'), 
            ObjectList(StandardPage.promote_panels, heading='promote'),
            ObjectList(StandardPage.settings_panels, heading='settings'),
        ])

    def get_context(self, request):
        context = super(NewsPage, self).get_context(request)
        related_news = self.paginate(request, self.get_related_news, size=5)
        gallery_images = self.paginate(request, self.get_gallery, size=1)
        context['related_news'] = related_news
        context['gallery_images'] = gallery_images
        return context
    
    class Meta:
        verbose_name = 'News Page'
        verbose_name_plural = 'News Page'

class EventGallery(GalleryImageBase):
    page = ParentalKey(EventPage, on_delete=models.CASCADE, related_name='gallery_images')

class NewsGallery(GalleryImageBase):
    page = ParentalKey(NewsPage, on_delete=models.CASCADE, related_name='gallery_images')

class NewsEventsIndexPage(StandardPage):

    gp_pg_size = 4
    news_pg_size = 4
    event_pg_size = 4
    upcoming_pg_size = 4
    past_event_pg_size = 4

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

    subpage_types = ['NewsPage', 'EventPage']

    content_panels =  [
        StreamFieldPanel('body'),
    ]

    edit_handler = TabbedInterface([
            ObjectList(standard_page_content_panels, heading='page & hero'),
            ObjectList(content_panels, heading='content'), 
            ObjectList(StandardPage.promote_panels, heading='promote'),
            ObjectList(StandardPage.settings_panels, heading='settings'),
        ])
    
    def get_upcoming_events(self):
        return EventPage.objects.filter(date_time__gt=datetime.datetime.now()).live().descendant_of(self).order_by('-first_published_at')

    def get_past_events(self):
        return EventPage.objects.filter(date_time__lt=datetime.datetime.now()).live().descendant_of(self).order_by('-first_published_at')

    def get_events(self):
        return EventPage.objects.live().descendant_of(self).order_by('-first_published_at')

    # get news for the past week for the past week
    def get_latest_news(self):
        today = datetime.date.today()
        a_week_ago = today - datetime.timedelta(days=7)
        return NewsPage.objects.live().descendant_of(self).order_by('-first_published_at')
        # NewsPage.objects.filter(date__range=[today, a_week_ago]).live().descendant_of(self).order_by('-first_published_at')

    def get_news(self, **kwargs):
        return NewsPage.objects.filter().live(**kwargs).descendant_of(self).order_by('-first_published_at')

    # Allows child objects to be accessible via the
    # template. We can use this on the HomePage to display child items of featured
    # content
    # def children(self):
    #     return self.get_children().specific().live()

    # Returns the above to the get_context method that is used to populate the template
    def get_context(self, request):
        context = super(NewsEventsIndexPage, self).get_context(request)

        news = self.paginate(request, self.get_news, size=self.news_pg_size)
        events = self.paginate(request, self.get_events, size=self.event_pg_size)
        latest_news = self.paginate(request, self.get_latest_news, size=self.gp_pg_size)
        past_events = self.paginate(request, self.get_past_events, size=self.past_event_pg_size)
        upcoming_events = self.paginate(request, self.get_upcoming_events, size=self.upcoming_pg_size)

        context['news'] = news
        context['events'] = events
        context['latest_news'] = latest_news
        context['past_events'] = past_events
        context['upcoming_events'] = upcoming_events

        return context

    class Meta:
        verbose_name = 'News & Events Index Page'
        verbose_name_plural = 'News & Events Index Page'
