from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Executive

# @modeladmin_register
class ExecutiveAdmin(ModelAdmin):
    model = Executive
    menu_icon = 'group'
    menu_order = 200
    menu_label = 'Executives'
    search_fields = ('name', )
    list_filter = ('featured', )