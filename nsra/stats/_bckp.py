from django.urls import reverse
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem


@hooks.register('register_admin_menu_item')
def register_data_menu_item():
  return MenuItem('Data Upload', reverse('data_upload_view'), classnames='icon icon-code', order=10000)

def data_upload_view(request):
    template = "stats/data_upload.html"
    context = {}
    return render(request, template, context)


@hooks.register('register_admin_urls')
def urlconf_time():
  return [
    url(r'^data-upload-centre/$', data_upload_view, name='data_upload_view'),
  ]
