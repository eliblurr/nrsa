from django import template
from wagtail.core.models import Page, Site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nsra.base.models import CopyrightText, SocialGroup, Contact, RelatedOrganization

register = template.Library()

@register.inclusion_tag('tags/related_organization.html', takes_context=True)
def get_related_organization(context):
    return context

@register.inclusion_tag('tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=1)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }

# @register.inclusion_tag('some-html-file-path', takes_context=True)
# def get_footer_text(context):
#     footer = FooterText.objects.filter(featured=True).first()
#     footer_text = footer.body if footer else ""
#     return {
#         'footer_text': footer_text,
#     }

# @register.inclusion_tag('some-html-file-path', takes_context=True)
# def get_copyright_text(context):
#     copyright_object = CopyrightText.objects.filter(featured=True).first()
#     copyright_text = copyright_object.body if copyright_object else ""
#     return {
#         'copyright_text': copyright_text,
#     }

# @register.inclusion_tag('some-html-file-path', takes_context=True)
# def get_socials(context):
#     socials = {}
#     group = SocialGroup.objects.filter(featured=True).first()
#     if group:
#         socials = {
#             'twitter': group.twitter,
#             'facebook': group.facebook,
#             'instagram': group.instagram,
#         }
#     return socials

# @register.inclusion_tag('some-html-file-path', takes_context=True)
# def get_contact(context):
#     contact = {}
#     group = Contact.objects.filter(featured=True).first()
#     if contact:
#         contact = {
#             'phone': group.phone,
#             'email': group.email,
#             'ghana_post': group.ghana_post,
#         }
#     return contact
