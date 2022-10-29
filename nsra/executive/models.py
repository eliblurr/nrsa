from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from nsra.base.models import BaseModel

@register_snippet
class Executive(BaseModel):
    name = models.CharField(max_length=1000)
    position = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    email = models.EmailField(max_length=1000, blank=True, null=True)
    twitter = models.URLField(max_length=10000, blank=True, null=True)
    facebook = models.URLField(max_length=10000, blank=True, null=True)
    instagram = models.URLField(max_length=10000, blank=True, null=True)
    linked_in = models.URLField(max_length=10000, blank=True, null=True)
    pinterest = models.URLField(max_length=10000, blank=True, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('position'),
            FieldPanel('featured'),
            ImageChooserPanel('image'),
        ], heading="Executive Information"),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('twitter'),
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('linked_in'),
            FieldPanel('pinterest'),
        ], heading="Social Links")
    ]

    def __str__(self):
        return self.name
