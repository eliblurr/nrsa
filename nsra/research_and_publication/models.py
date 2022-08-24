from django.db import models
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList, PageChooserPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from wagtail.documents.models import Document, AbstractDocument
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from nsra.base.models import GalleryImageBase, StandardPage
from wagtail.snippets.models import register_snippet
from wagtail.core.blocks import StreamBlock
from nsra.base.blocks import BaseStreamBlock
from nsra.base.models import BaseModel
from django.db.models import Count
from wagtail.search import index
from wagtail.api import APIField
from django import forms

standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

class ResearchCategory(models.Model):
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
        verbose_name_plural = 'Research Categories'

class PublicationCategory(models.Model):
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
        verbose_name_plural = 'Publication Categories'

class ResearchTag(TaggedItemBase):
    content_object = ParentalKey(
        'ResearchPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class PublicationTag(TaggedItemBase):
    content_object = ParentalKey(
        'PublicationPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class ResearchPage(StandardPage):
    date = models.DateField("Post date")
    headline = models.CharField(blank=True, max_length=250)
    categories = ParentalManyToManyField('research_and_publication.ResearchCategory', blank=True, related_name='research')
    tags = ClusterTaggableManager(through=ResearchTag, blank=True)

    subpage_types = []
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_related_research(self):
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
        context = super(ResearchPage, self).get_context(request)
        related_research = self.paginate(request, self.get_related_research, size=5)
        gallery_images = self.paginate(request, self.get_gallery, size=1)
        context['related_research'] = related_research
        context['gallery_images'] = gallery_images
        return context

class PublicationPage(StandardPage):
    date = models.DateField("Post date")
    headline = models.CharField(blank=True, max_length=250)
    categories = ParentalManyToManyField('research_and_publication.PublicationCategory', blank=True, related_name='publication')
    tags = ClusterTaggableManager(through=PublicationTag, blank=True)

    subpage_types = []

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_related_publications(self):
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
        context = super(PublicationPage, self).get_context(request)
        related_publications = self.paginate(request, self.get_related_publications, size=5)
        gallery_images = self.paginate(request, self.get_gallery, size=1)
        context['related_publications'] = related_publications
        context['gallery_images'] = gallery_images
        return context

class ResearchGallery(GalleryImageBase):
    page = ParentalKey(ResearchPage, on_delete=models.CASCADE, related_name='gallery_images')

class PublicationGallery(GalleryImageBase):
    page = ParentalKey(PublicationPage, on_delete=models.CASCADE, related_name='gallery_images')

class ResearchPublicationIndexPage(StandardPage):

    research_pg_size = 8
    publication_pg_size = 8

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

    subpage_types = ['ResearchPage', 'PublicationPage']

    content_panels =  [
        StreamFieldPanel('body'),
    ]

    edit_handler = TabbedInterface([
            ObjectList(standard_page_content_panels, heading='page & hero'),
            ObjectList(content_panels, heading='content'), 
            ObjectList(StandardPage.promote_panels, heading='promote'),
            ObjectList(StandardPage.settings_panels, heading='settings'),
        ])

    def get_research_categories(self, **kwargs):
        return ResearchCategory.objects.all().annotate(research_count=Count('research__id')).order_by('research_count')

    def get_publication_categories(self, **kwargs):
        return PublicationCategory.objects.all().annotate(publication_count=Count('publication__id')).order_by('publication_count')
    
    # Returns a queryset of ResearchPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_research(self, **kwargs):
        return ResearchPage.objects.filter(**kwargs).live().descendant_of(self).order_by('-first_published_at')

    # Returns a queryset of PublicationPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_publication(self, **kwargs):
        return PublicationPage.objects.filter(**kwargs).live().descendant_of(self).order_by('-first_published_at')

    def get_group_research(self, pk):
        return ResearchCategory.objects.get(pk=pk).research.live().descendant_of(self)

    def get_group_publication(self, pk):
        return PublicationCategory.objects.get(pk=pk).publication.live().descendant_of(self)

    def get_grouped_research(self, request):
        return [
            {
                'category': category,
                'pages': self.paginate(request, self.get_group_research, pk=category.pk)

            } for category in self.get_research_categories()
        ]

    def get_grouped_publication(self, request):
        return [
            {
                'publication': publication,
                'pages': self.paginate(request, self.get_group_publication, pk=publication.pk)

            } for publication in self.get_publication_categories()
        ]

    # Allows child objects (e.g. PublicationPage objects) to be accessible via the
    # template. We can use this on the HomePage to display child items of featured
    # content
    # def children(self):
    #     return self.get_children().specific().live()

    # Returns the above to the get_context method that is used to populate the template
    def get_context(self, request):
        context = super(ResearchPublicationIndexPage, self).get_context(request)

        research = self.paginate(request, self.get_research, size=self.research_pg_size)
        publication = self.paginate(request, self.get_publication, size=self.publication_pg_size)
        research_categories = self.paginate(request, self.get_research_categories)
        publication_categories = self.paginate(request, self.get_publication_categories)
        grouped_publication = self.get_grouped_publication(request)
        grouped_research = self.get_grouped_research(request)

        context['research'] = research
        context['publications'] = publication
        context['research_categories'] = research_categories
        context['publication_categories'] = publication_categories
        context['grouped_publication'] = grouped_publication
        context['grouped_research'] = grouped_research

        return context
