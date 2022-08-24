from django import template
from wagtail.documents import get_document_model

documents = get_document_model()
register = template.Library()

@register.inclusion_tag('tags/documents.html', takes_context=True)
def get_documents(context):
    docs = documents.objects.filter(feature_on_research_and_publication=True).all()
    return {
        'documents': docs,
        'request': context['request'],
    }