from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from nsra.research_and_publication.models import PublicationCategory, ResearchCategory
from .models import SocialGroup, Contact, RelatedOrganization
from nsra.executive.wagtail_hooks import ExecutiveAdmin
from nsra.core_functions.models import CoreFunction
from nsra.activity.models import ActivityCategory
from nsra.regional_profiles.models import Regions
from nsra.galleries.models import Gallery

class RegionAdmin(ModelAdmin):
    model = Regions
    search_fields = ('name', )
    list_filter = ('name', )

class CoreFunctionAdmin(ModelAdmin):
    model = CoreFunction
    search_fields = ('title', )
    list_filter = ('featured', )

class GalleryAdmin(ModelAdmin):
    model = Gallery
    search_fields = ('name', )
    # list_filter = ('featured', )

class RelatedOrganizationAdmin(ModelAdmin):
    model = RelatedOrganization
    search_fields = ('name', )
    list_filter = ('featured', )

class SocialGroupAdmin(ModelAdmin):
    model = SocialGroup
    search_fields = ('name', )
    list_filter = ('featured', )

class ContactAdmin(ModelAdmin):
    model = Contact
    search_fields = ('name', 'email', 'phone', 'ghana_post')
    list_filter = ('featured', )

class PublicationCategoryAdmin(ModelAdmin):
    menu_label = 'Publication'
    model = PublicationCategory
    search_fields = ('name')
    menu_icon = 'folder-open-inverse'

class ResearchCategoryAdmin(ModelAdmin):
    menu_label = 'Research'
    model = ResearchCategory
    search_fields = ('name')
    menu_icon = 'folder-open-inverse'

class ActivityCategoryAdmin(ModelAdmin):
    menu_label = 'Activity'
    model = ActivityCategory
    search_fields = ('name')
    menu_icon = 'folder-open-inverse'

class SiteThemeAdminGroup(ModelAdminGroup):
    menu_label = 'Page Data'
    menu_icon = 'placeholder'  # change as required
    menu_order = 200  # will put in 1st place (004 being 4th, 100 2nd)
    items = (RelatedOrganizationAdmin, CoreFunctionAdmin, ExecutiveAdmin, RegionAdmin, GalleryAdmin)

class CategoryAdminGroup(ModelAdminGroup):
    menu_label = 'Categories'
    menu_icon = 'grip'  # change as required
    menu_order = 300  # 100 will put in 1st place (004 being 4th, 100 2nd)
    items = (ResearchCategoryAdmin, PublicationCategoryAdmin, ActivityCategoryAdmin)

modeladmin_register(SiteThemeAdminGroup)
modeladmin_register(CategoryAdminGroup)