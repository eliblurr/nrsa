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
from django.core.serializers.json import DjangoJSONEncoder
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.contrib.forms.models import AbstractForm
from  .data_extractor import format_1, format_2, main
from django.utils.functional import cached_property
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.images.fields import WagtailImageField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.blocks import StreamBlock
from django.shortcuts import redirect
from django.http import HttpResponse
from wagtail.search import index
from wagtail.api import APIField
from . import spreadsheet_parser
from django import forms
import json, logging
from wagtail.contrib.forms.models import (
    AbstractEmailForm, 
    AbstractFormField, 
    AbstractFormSubmission, 
    FORM_FIELD_CHOICES
)

standard_page_content_panels = [item for item in StandardPage.content_panels if not(isinstance(item, FieldPanel) and item.field_name=='body')]

class StatisticsIndexPage(StandardPage):

    subpage_types = []

    class Meta:
        verbose_name = "Statistics Page"

class FormField(AbstractFormField):
    page = ParentalKey('DataFormPage', related_name='custom_form_fields',
            on_delete=models.CASCADE)
    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        choices=FORM_FIELD_CHOICES + (('fileupload', 'File Upload'),)
    )

class DataFormBuilder(FormBuilder):

    def create_fileupload_field(self, field, options):
        return forms.FileField(**options)

class DataFormPage(AbstractForm):
    form_builder = DataFormBuilder

    content_panels = AbstractForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),

    ]

    @cached_property
    def stats_page(self):
        return self.get_parent().specific

    def serve(self, request):
        if request.user.is_anonymous:
            return redirect('unauthorized')
        return super().serve(request)

    def get_context(self, request, *args, **kwargs):
        context = super(DataFormPage, self).get_context(request, *args, **kwargs)
        context["stats_page"] = self.stats_page
        return context

    def get_form_fields(self):
        return self.custom_form_fields.all()

    @staticmethod
    def get_file_title(filename):
        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()
        return ''

    def process_form_submission(self,form):
        """
        Accepts form instance with submitted data, user and page.
        Creates submission instance.
        You can override this method if you want to have custom creation logic.
        For example, if you want to save reference to a user.
from wagtail.admin.forms import WagtailAdminModelForm

class Foo(models.Model):
    ...
    base_form_class = FooForm


class FooForm(WagtailAdminModelForm):
    def clean(self):
        data = self.cleaned_data['recipients']
        if "fred@example.com" not in data:
            raise ValidationError("You have forgotten about Fred!")
        return data


        from django.core.exceptions import ValidationError

        class Foo(models.Model):
            ...
            def clean(self):
                if "fred@example.com" not in self.recipients:
                    raise ValidationError(
                        {'recipients': _("You have forgotten about Fred!")}
                    )



        """

        option = form.cleaned_data['options']

        file_form_fields = [field.clean_name for field in self.get_form_fields()
                        if field.field_type == 'fileupload']

        for (field_name, field_value) in form.cleaned_data.items():
            if field_name in file_form_fields:
                if option == "First":
                    csv_str = spreadsheet_parser.file_ext_check(field_value)
                    format_1(csv_str)

                elif option == "Second":
                    logging.info(f"{field_name} Received")
                    #filename = '.'.join(request.FILES['file'].name.split('.')[:-1])
                    filename = '.'.join(field_value.name.split('.')[:-1])
        			#format_2(request.FILES['file'], filename)
                    format_2(field_value, filename)

                elif option=="Standard":
                    filename = '.'.join(field_value.name.split('.')[:-1])
                    logging.info(f"{filename} Received")
                    main(field_value, filename)

                # store a reference to the pk (as this can be converted to JSON)
                form.cleaned_data[field_name] = 111#uploaded_file.pk
        return self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
        )


from .data_upload_models import *