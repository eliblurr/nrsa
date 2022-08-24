from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from birdsong.options import CampaignAdmin
from birdsong.models import Contact
from .models import Newsletter

class NewsletterAdmin(CampaignAdmin):
    campaign = Newsletter
    menu_label = 'Newsletters'
    menu_icon = 'mail'
    contact_class = Contact

class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Subscriptions'
    menu_icon = 'user'
    list_diplay = ('email')

@modeladmin_register
class CategoryAdminGroup(ModelAdminGroup):
    menu_label = 'Newsletter'
    menu_icon = 'mail'  # change as required
    menu_order = 400  # will put in 1st place (004 being 4th, 100 2nd)
    items = (NewsletterAdmin, ContactAdmin)