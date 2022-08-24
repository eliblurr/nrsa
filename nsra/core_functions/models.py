from django.db import models
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel, FieldRowPanel, TabbedInterface, ObjectList
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet
from wagtail.core.blocks import StreamBlock
from nsra.base.models import StandardPage
from wagtail.search import index
from django import forms

@register_snippet
class CoreFunction(models.Model):
    title = models.CharField(max_length=1000)
    subtitle = models.CharField(max_length=1000, null=True, blank=True)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=False, blank=False,
        on_delete=models.CASCADE, related_name='+'
    )
    
    body = RichTextField(blank=False)
    featured = models.BooleanField(default=False)
    
    sub_functions = models.ManyToManyField('self', blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subtitle'),
            FieldPanel('body'),
            ImageChooserPanel('icon'),
        ], heading="Content Information"),

        FieldPanel('sub_functions'), #, widget=forms.CheckboxSelectMultiple)
        
        FieldPanel('featured'),      
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Core Functions'

class CoreFunctionIndexPageOrderable(Orderable):
    page = ParentalKey('core_functions.CoreFunctionIndexPage', on_delete=models.CASCADE, related_name='functions')
    function = models.ForeignKey('core_functions.CoreFunction', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('function'),
    ]

class CoreFunctionIndexPage(StandardPage):

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

    subpage_types = []

    search_fields = StandardPage.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
    ]

    standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

    content_panels =  [
        StreamFieldPanel('body'),
    ]

    function_panels = [
        InlinePanel('functions', min_num=1),
    ]

    edit_handler = TabbedInterface([
            ObjectList(standard_page_content_panels, heading='page & hero'),
            ObjectList(content_panels, heading='content'), 
            ObjectList(function_panels, heading='Page Functions'), 
            ObjectList(StandardPage.promote_panels, heading='promote'),
            ObjectList(StandardPage.settings_panels, heading='settings'),
        ])

    def get_functions(self):
        return self.functions.filter(function__featured=True).all()
       
    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(CoreFunctionIndexPage, self).get_context(request)
        functions = self.get_functions()
        context['featured_functions'] = functions
        return context
