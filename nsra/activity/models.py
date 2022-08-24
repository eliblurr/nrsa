from django.db import models
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList, StreamFieldPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from nsra.base.models import GalleryImageBase, StandardPage, BaseModel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import StreamBlock
from wagtail.search import index
from wagtail.api import APIField
from django import forms

standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

class ActivityCategory(BaseModel):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Activity Categories/Sections'

class ActivityTag(TaggedItemBase):
    content_object = ParentalKey(
        'ActivityPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class ActivityPage(StandardPage):
    date = models.DateField("Post date")
    headline = models.CharField(blank=True, max_length=250)
    categories = ParentalManyToManyField('activity.ActivityCategory', blank=True, related_name='activities')
    tags = ClusterTaggableManager(through=ActivityTag, blank=True)

    subpage_types = []

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_related_activities(self):
        return self.__class__.objects.filter(
            models.Q(
                categories__in=self.categories.all()
            ) | models.Q(
                tags__in=self.tags.all()
            )
        ).distinct().exclude(pk=self.pk).live()

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
        ], heading="body"),

        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
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
        context = super(ActivityPage, self).get_context(request)
        related_activities = self.paginate(request, self.get_related_activities, size=5)
        gallery_images = self.paginate(request, self.get_gallery, size=1)
        context['related_activities'] = related_activities
        context['gallery_images'] = gallery_images
        return context

class ActivityGallery(GalleryImageBase):
    page = ParentalKey('activity.ActivityPage', on_delete=models.CASCADE, related_name='gallery_images')

class ActivityIndexPage(StandardPage):

    gp_pg_size = 4

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

    subpage_types = ['ActivityPage']

    content_panels =  [
        StreamFieldPanel('body'),
    ]

    edit_handler = TabbedInterface([
            ObjectList(standard_page_content_panels, heading='page & hero'),
            ObjectList(content_panels, heading='content'), 
            ObjectList(StandardPage.promote_panels, heading='promote'),
            ObjectList(StandardPage.settings_panels, heading='settings'),
        ])

    def get_activities(self):
        return ActivityPage.objects.live().descendant_of(self).order_by('-first_published_at')
    
    def get_categories(self):
        return ActivityCategory.objects.all().order_by('-created')

    def get_group_activities(self, pk):
        return ActivityCategory.objects.get(pk=pk).activities.live()
        # .descendant_of(self)

    def get_grouped_activities(self, request): 
        return [
            {
                'category': category,
                'pages': self.paginate(request, self.get_group_activities, pk=category.pk, size=self.gp_pg_size)

            } for category in self.get_categories()
        ]
       
    def get_context(self, request):
        context = super(ActivityIndexPage, self).get_context(request)

        activities = self.paginate(request, self.get_activities)
        categories = self.paginate(request, self.get_categories)
        grouped_activities = self.get_grouped_activities(request)

        context['activities'] = activities
        context['categories'] = categories
        context['grouped_activities'] = grouped_activities

        return context