from django.db import models
from wagtail.search import index
from .validators import phone_validator
from wagtail.core.models import Page, Orderable
from django.core.exceptions import ValidationError
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm, AbstractForm
from nsra.base.blocks import BaseStreamBlock, ParagraphStreamBlock, ImageBlock
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.documents.models import Document, AbstractDocument
from wagtail.documents.models import Document, AbstractDocument
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from wagtail.core.blocks import StreamBlock
from modelcluster.fields import ParentalKey
from wagtailseo.models import SeoMixin
from nsra.base.choices import COLORS
from .blocks import BaseStreamBlock
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

@register_setting
class Settings(BaseSetting):

    #  logo
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )
    favicon = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    caption = models.CharField(blank=True, max_length=250)

    # contact

    contact = models.ForeignKey(
        'base.Contact', on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )

    # copyright

    copyright_text = RichTextField(null=True, blank=True)

    # social group

    social = models.ForeignKey(
        'base.SocialGroup', on_delete=models.CASCADE, related_name='+', null=True, blank=True
    ) # required

    # footer text

    footer = models.ForeignKey(
        'base.Footer', on_delete=models.CASCADE, related_name='+', null=True, blank=True
    ) # required

    class Meta:
        verbose_name = 'Logo'

    site_contact_panels = [
        SnippetChooserPanel('contact'),
    ]

    site_logo_panels = [  
        ImageChooserPanel('logo'),
        ImageChooserPanel('favicon'),
        FieldPanel('caption'),
        FieldPanel('name'),
    ]

    site_copyright_footer_text = [
        SnippetChooserPanel('footer'),
        FieldPanel('copyright_text', classname="full"),
    ]

    site_social_group = [
        SnippetChooserPanel('social'),
    ]

    class Meta:
        verbose_name = 'Site Settings'

    edit_handler = TabbedInterface([
        ObjectList(site_logo_panels, heading='Logo'),
        ObjectList(site_contact_panels, heading='Contact'),
        ObjectList(site_social_group, heading='Social'),
        ObjectList(site_copyright_footer_text, heading='Footer/Copyright Texts'),
    ])

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class GalleryImageBase(Orderable):
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    caption = models.CharField(blank=True, null=True, max_length=250)

    panels = [
        ImageChooserPanel('image', classname="collapsible collapsed"),
        FieldPanel('caption', classname="collapsible"),
    ]

    class Meta:
        abstract = True

class StandardPage(SeoMixin, Page):
    hero_title = models.CharField(help_text='Title to display in hero, if null page.title will be used', blank=True, max_length=250)
    
    hero_sub_title = models.CharField(help_text='Subtitle to display in hero, if null no subtitle will be rendered', blank=True, max_length=250)
    hero_description = models.CharField(help_text='Description to display in hero, if null no description will be rendered', blank=True, max_length=250)
    hero_external_link = models.URLField(help_text='Link that points to external resource',max_length=10000, null=True, blank=True)


    hero_cta = models.CharField(
        verbose_name='Hero CTA',
        max_length=255,
        help_text='Text to display on Call to Action',
        default='CTA',
        null=True,
        blank=True,
    )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero CTA link',
        help_text='Choose a page to link to for the Call to Action'
    )

    hero_external = models.CharField(
        verbose_name='Hero External Link',
        max_length=255,
        help_text='Text to display on external link CTA',
        default='CTA',
        null=True,
        blank=True,
    )


    body = RichTextField(blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    # Breadcrumb

    # SeoMixin.seo_panels

    promote_panels = SeoMixin.seo_panels 
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title', classname="collapsible"),
            FieldPanel('hero_sub_title', classname="collapsible"),
            FieldPanel('hero_description', classname="collapsible"),
            MultiFieldPanel([
                FieldPanel('hero_external', classname="collapsible"),
                FieldPanel('hero_external_link', classname="collapsible"),
            ], heading=""),
            MultiFieldPanel([
                FieldPanel('hero_cta'),
                PageChooserPanel('hero_cta_link'),
            ], heading="")
        ], heading=""),
        ImageChooserPanel('hero_image', classname="collapsible"),
        FieldPanel('body', classname="collapsible"),
    ]

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, func, *args, size=12, **kwargs):
        page = request.GET.get('page')
        paginator = Paginator(func(**kwargs), size)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        return super().get_context(request)

    class Meta:
        abstract = True

class FeaturedModel(BaseModel):
    '''
    This model allows other models to set default object.
    Only one object can have featured=True at any given time
    '''
    featured = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def clean(self):
        # raise exception
        # case = ((self.featured),(self.__class__.objects.filter(featured=True).all().count() > 0))
        # if all(case) :
        #     raise ValidationError('cannot have more than one featured objects')
        # or do override
        self.__class__.objects.filter(featured=True).update(featured=False)
            
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class FormField(AbstractFormField):
    """
    Wagtailforms is a module to introduce simple forms on a Wagtail site. It
    isn't intended as a replacement to Django's form support but as a quick way
    to generate a general purpose data-collection form or contact form
    without having to write code. We use it on the site for a contact form. You
    can read more about Wagtail forms at:
    https://docs.wagtail.org/en/stable/reference/contrib/forms/index.html
    """
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)

class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )


    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        ImageChooserPanel('hero_image'),
        StreamFieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),

        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

@register_snippet
class RelatedOrganisationCategories(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=5000, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Related Organisation Category'
        verbose_name_plural = 'Related Organisation Categories'

@register_snippet
class RelatedOrganization(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=10000)
    featured = models.BooleanField(default=False)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    categories = ParentalManyToManyField('RelatedOrganisationCategories', blank=True, related_name='related_organizations')

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('url'),
        ], heading="Organization Information"),
        FieldPanel('featured'),
        ImageChooserPanel('image'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
    ]

    # objects = FeaturedManager()

    def __str__(self):
        return self.name

@register_snippet
class SocialGroup(BaseModel):
    name = models.CharField(max_length=255)
    twitter = models.URLField(max_length=10000, null=True, blank=True)
    facebook = models.URLField(max_length=10000, null=True, blank=True)
    instagram = models.URLField(max_length=10000, null=True, blank=True)
    pinterest = models.URLField(max_length=10000, null=True, blank=True)
    linked_in = models.URLField(max_length=10000, null=True, blank=True)
    youtube = models.URLField(max_length=10000, null=True, blank=True)
    tumblr = models.URLField(max_length=10000, null=True, blank=True)
    reddit = models.URLField(max_length=10000, null=True, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('twitter'),
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('pinterest'),
            FieldPanel('linked_in'),
            FieldPanel('youtube'),
            FieldPanel('tumblr'),
            FieldPanel('reddit'),
        ], heading="Social Links"),
        MultiFieldPanel([
            FieldPanel('name'),
        ], heading="Meta"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['twitter', 'facebook', 'instagram']

class FooterLink(Orderable): 
    page = ParentalKey('base.Footer', on_delete=models.CASCADE, related_name='links')
    link_title = models.CharField(
        max_length=255,
        verbose_name='link title',
        null=True,
        blank=True,
    )
    # hero_external_link = models.URLField(help_text='Link that points to external resource',max_length=10000, null=True, blank=True)

    link_url = models.CharField(
        max_length=500,
        blank=True
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Link',
        help_text='Page links to display in footer'
    )

    panels = [
        FieldPanel('link_title'),
        FieldPanel('link_url'),
        PageChooserPanel('link_page'),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'

@register_snippet
class Footer(ClusterableModel): 
    name = models.CharField(
        max_length=255,
        verbose_name='name',
        help_text='Name to search/identify footer by'
    )
    text = RichTextField()

    panels = [
        FieldPanel('name'),
        FieldPanel('text'),
        InlinePanel('links', label="add footer link")
    ]

    search_fields = [
        index.SearchField('name'),
        index.SearchField('text'),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Footer'

@register_snippet
class CopyrightText(BaseModel): 
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return f"Copyright text {self.pk}"

    class Meta:
        verbose_name_plural = 'Copyright text'

@register_snippet
class Contact(BaseModel):
    name = models.CharField(max_length=255)
    body = RichTextField(null=True, blank=True)
    phone = models.CharField(validators=[phone_validator], max_length=17, blank=True)
    email = models.EmailField(max_length=254)
    ghana_post = models.CharField(max_length=255)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
        ], heading="Meta"),
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Contant Information"),
        FieldPanel('ghana_post'),
        FieldPanel('body'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contacts'

class CustomDocument(AbstractDocument):

    feature_on_research_and_publication = models.BooleanField(blank=False, null=False, default=False)
    link_title = models.CharField(max_length=500, blank=True, null=True)

    admin_form_fields = Document.admin_form_fields + (
        # Add all custom fields names to make them appear in the form:
        'link_title',
        'feature_on_research_and_publication'
    )

    def __str__(self):
        if self.link_title:
            return self.link_title
        # print(dir(self.file), type(self.file))
        return self.file.name

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


''' STATISTICS '''

from django.db import models
from django.db.models import Sum, Value, F
from django.utils import timezone
from datetime import datetime

# Create your models here.
class AnnotationManager(models.Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = kwargs

    def get_queryset(self):
        return super().get_queryset().annotate(**self.annotations)


months = (('January', 'January'), ('February', 'February'), ('March', 'March'),
          ('April', 'April'), ('May', 'May'), ('June', 'June'),
          ('July', 'July'), ('August', 'August'), ('September', 'September'),
          ('October', 'October'), ('November', 'November'), ('December', 'December'))

year = ((2020, 2020), (2021, 2021))


class DataSet(models.Model):
    File = models.FileField(upload_to='Data_sources')
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"Data for {self.id}"


class Common(models.Model):
    date = models.DateField(auto_now_add=True)
    year = models.IntegerField(choices=year)
    month = models.CharField(choices=months, max_length=9)
    region = models.CharField(max_length=30, default='')
    injured = models.IntegerField(default=0)
    killed = models.IntegerField(default=0)

    SearchableFields = ['year', 'month', 'region']

    class Meta:
        abstract = True


class ReportedCase(models.Model):
    date = models.DateField(auto_now_add=True)
    year = models.IntegerField(choices=year, default=datetime.now().strftime("%Y"))
    month = models.CharField(choices=months, max_length=10, default=datetime.now().strftime("%B"))
    region = models.CharField(max_length=30, default='')
    fatal = models.IntegerField(default=0)
    serious = models.IntegerField(default=0)
    minor = models.IntegerField(default=0)
    RC_total = None

    SearchableFields = ['year', 'month', 'region']

    objects = AnnotationManager(RC_total=F('fatal') + F('serious') + F('minor'))

    def __str__(self):
        return f'{self.month}, {self.year}: Reported Cases in {self.region}'


class Injured(models.Model):
    date = models.DateField(auto_now_add=True)
    year = models.IntegerField(choices=year, default=datetime.now().strftime("%Y"))
    month = models.CharField(choices=months, max_length=10, default=datetime.now().strftime("%B"))
    region = models.CharField(max_length=30, default='')
    injured = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.month}, {self.year}: Persons injured in {self.region}'


class Commercial(Common):
    bus = models.IntegerField(default=0)
    minor_bus = models.IntegerField(default=0)
    truck = models.IntegerField(default=0)
    taxi = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
    Com_total = None

    objects = AnnotationManager(Com_total=F('bus') + F('minor_bus') + F('truck') + F('taxi') + F('other'))

    def __str__(self):
        return f'{self.month}, {self.year}: Commercial Vehicles involved in {self.region}'


class Private(Common):
    minibus = models.IntegerField(default=0)
    salon = models.IntegerField(default=0)
    suv = models.IntegerField(default=0)
    govt = models.IntegerField(default=0)
    truck = models.IntegerField(default=0)
    Priv_total = None

    objects = AnnotationManager(Priv_total=F('minibus') + F('salon') + F('suv') + F("govt"))

    def __str__(self):
        return f'{self.month} , {self.year}: Private Vehicles involved in {self.region}'


class Cycle(Common):
    m_cycle = models.IntegerField(default=0)
    bicycles = models.IntegerField(default=0)
    handcart = models.IntegerField(default=0)
    tricycle = models.IntegerField(default=0)
    Cyc_total = None

    objects = AnnotationManager(Cyc_total=F('m_cycle') + F('bicycles') + F('handcart') + F('tricycle'))

    def __str__(self):
        return f'{self.month}, {self.year}: Cycles involved in {self.region}'

class TotalKilled(Common):
    male_over18 = models.IntegerField(default=0)
    male_under18 = models.IntegerField(default=0)
    female_over18 = models.IntegerField(default=0)
    female_under18 = models.IntegerField(default=0)
    Tk_total = None

    objects = AnnotationManager(Tk_total=F('male_over18')+F('male_under18')+F('female_over18')+F('female_under18'))

    def __str__(self):
        return f'{self.month}, {self.year}: Total Killed in {self.region}'

class Pedestrian(Common):
    Ped_total = None

    objects = AnnotationManager(Ped_total=F('injured') + F('killed'))

    def __str__(self):
        return f'{self.month}, {self.year}: Pedestrians knocked down in {self.region}'
