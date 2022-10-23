from django.db import models
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel, FieldRowPanel, TabbedInterface, ObjectList
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.admin.edit_handlers import InlinePanel as BaseInlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from nsra.base.models import GalleryImageBase, StandardPage
from wagtail.core.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from wagtail.core.blocks import StreamBlock
from wagtail.search import index
from wagtail.api import APIField
from django import forms
import json

standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

class InlinePanel(BaseInlinePanel):
    def widget_overrides(self):
        widgets = {}
        child_edit_handler = self.get_child_edit_handler()
        for handler_class in child_edit_handler.children:
            widgets.update(handler_class.widget_overrides())
        widget_overrides = {self.relation_name: widgets}
        return widget_overrides
    
class GalleryIndexPage(StandardPage):

    body = StreamField(BaseStreamBlock(),null=True,blank=True)
    content_panels =  [StreamFieldPanel('body'),]

    galleries_panels = [
        InlinePanel('galleries', classname="collapse"),
    ]

    # class InlinePanel(relation_name, panels=None, heading='', label='', min_num=None, max_num=None, heading='', classname='', help_text='', /, *, classname='', help_text='')

    edit_handler = TabbedInterface([
        ObjectList(standard_page_content_panels, heading='page & hero'),
        ObjectList(galleries_panels, heading='Galleries'), 
        ObjectList(content_panels, heading='content'), 
        ObjectList(StandardPage.promote_panels, heading='promote'),
        ObjectList(StandardPage.settings_panels, heading='settings'),
    ])

    def get_galleries(self):
        return Gallery.objects.filter(page=self.id)

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
        # galleries = self.paginate(request, self.get_galleries)
        context['galleries'] = self.get_galleries()
        return context

class Gallery(ClusterableModel, Orderable):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)
    page = ParentalKey(GalleryIndexPage, on_delete=models.CASCADE, related_name='galleries', null=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_image_count(self):
        return self.gallery_images.count()

    def get_images(self):
        a = [obj.image.get_rendition('original').url for obj in self.gallery_images.all()]
        print(json.dumps(a))
        return json.dumps(a)

    panels = [
        FieldPanel('name', classname="full"),
        FieldPanel('description', classname="full"),
        InlinePanel('gallery_images', classname="collapsed"),
    ]

    class Meta:
        verbose_name_plural = 'galleries'
        verbose_name = 'gallery'

    def __str__(self):
        return self.name

class GalleryImages(GalleryImageBase):
    gallery = ParentalKey(Gallery, on_delete=models.CASCADE, related_name='gallery_images', null=True)
    