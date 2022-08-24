from django.db import models
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel, FieldRowPanel, TabbedInterface, ObjectList
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.core.fields import RichTextField, StreamField
from nsra.base.models import GalleryImageBase, StandardPage
from wagtail.core.blocks import StreamBlock
from wagtail.search import index
from wagtail.api import APIField
from django import forms

standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

class GalleryPage(StandardPage):
    name = models.CharField(max_length=255, blank=True, null=True)

    subpage_types = []

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('title'),
    ]

    content_panels = [
        FieldPanel('name', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(standard_page_content_panels, heading='page & hero'),
        ObjectList(content_panels, heading='content'), 
        ObjectList(StandardPage.promote_panels, heading='promote'),
        ObjectList(StandardPage.settings_panels, heading='settings'),
    ])

class GalleryImages(GalleryImageBase):
    page = ParentalKey(GalleryPage, on_delete=models.CASCADE, related_name='gallery_images')

class GalleryIndexPage(StandardPage):

    body = StreamField(BaseStreamBlock(),null=True,blank=True)

    subpage_types = ['GalleryPage']
    content_panels =  [StreamFieldPanel('body'),]

    edit_handler = TabbedInterface([
        ObjectList(standard_page_content_panels, heading='page & hero'),
        ObjectList(content_panels, heading='content'), 
        ObjectList(StandardPage.promote_panels, heading='promote'),
        ObjectList(StandardPage.settings_panels, heading='settings'),
    ])

    def get_galleries(self,**kwargs):
        return GalleryPage.objects.filter(**kwargs).live().descendant_of(self).order_by('-first_published_at')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, func, *args, **kwargs):
        page = request.GET.get('page')
        paginator = Paginator(func(**kwargs), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(GalleryIndexPage, self).get_context(request)
        galleries = self.paginate(request, self.get_galleries)
        context['galleries'] = galleries
        return context
