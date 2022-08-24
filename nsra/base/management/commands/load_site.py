from django.core.files.storage import default_storage, FileSystemStorage
from django.core.management.base import BaseCommand
from django.core.management import call_command
from wagtail.core.models import Site, Page
from django.db import migrations
from django.conf import settings
from django.apps import apps
import os

class Command(BaseCommand):

    def create_homepage(self):
        # Get models
        ContentType = apps.get_model('contenttypes.ContentType')
        Page = apps.get_model('wagtailcore.Page')
        Site = apps.get_model('wagtailcore.Site')
        HomePage = apps.get_model('home.HomePage')

        # Delete the default homepage
        # If migration is run multiple times, it may have already been deleted
        Page.objects.filter(id=2).delete()

        # Create content type for homepage model
        homepage_content_type, __ = ContentType.objects.get_or_create(model='homepage', app_label='home')

        # Create a new homepage
        homepage = HomePage.objects.create(
            title="Home",
            draft_title="NSRA Site",
            slug='home',
            content_type=homepage_content_type,
            path='00010002',
            depth=2,
            numchild=0,
            url_path='/custom-home/',
        )

        # Create a site with the new homepage set as the root
        Site.objects.create(
            hostname='localhost', 
            root_page=homepage, 
            root_page_id=homepage.pk,
            is_default_site=True,
            site_name="NSRA"
        )

        f = Site.objects.first()
        print(dir(f))

        print(
            """
            &&&&&&&&&&&&&&&&&&&&&&&&&&
            &&    &&&  &&  &&  &&&&&&&        
            &&  &  &&  &&  &&  &&&&&&&   
            &&  &&  &  &&  &&  &&&&&&&     
            &&  &&     &&  &&      &&&
            &&&&&&&&&&&&&&&&&&&&&&&&&&     
            """
        )

    def remove_homepage(self):
        # Get models
        ContentType = apps.get_model('contenttypes.ContentType')
        HomePage = apps.get_model('home.HomePage')

        # Delete the default homepage
        # Page and Site objects CASCADE
        HomePage.objects.filter(slug='home', depth=2).delete()

        # Delete content type for homepage model
        ContentType.objects.filter(model='homepage', app_label='home').delete()

        # Wagtail creates default Site and Page instances during install, but we already have
        # them in the data load. Remove the auto-generated ones.
        if Site.objects.filter(hostname='localhost').exists():
            Site.objects.get(hostname='localhost').delete()
        if Page.objects.filter(title='Welcome to your new Wagtail site!').exists():
            Page.objects.get(title='Welcome to your new Wagtail site!').delete()

    def _copy_files(self, local_storage, path):
        """
        Recursively copy files from local_storage to default_storage. Used
        to automatically bootstrap the media directory (both locally and on
        cloud providers) with the images linked from the initial data (and
        included in MEDIA_ROOT).
        """
        directories, file_names = local_storage.listdir(path)
        for directory in directories:
           self._copy_files(local_storage, path + directory + '/')
        for file_name in file_names:
            with local_storage.open(path + file_name) as file_:
                default_storage.save(path + file_name, file_)
    
    def handle(self, *args, **options):
        fixtures_dir = os.path.join(settings.PROJECT_DIR, 'base', 'fixtures')
        fixture_file = os.path.join(fixtures_dir, 'site.json')

        print("Copying media files to configured storage...")
        local_storage = FileSystemStorage(os.path.join(fixtures_dir, 'media'))
        self._copy_files(local_storage, '')  # file storage paths are relative

        # Wagtail creates default Site and Page instances during install, but we already have
        # them in the data load. Remove the auto-generated ones.
        if Site.objects.filter(hostname='localhost').exists():
            Site.objects.get(hostname='localhost').delete()
        if Page.objects.filter(title='Welcome to your new Wagtail site!').exists():
            Page.objects.get(title='Welcome to your new Wagtail site!').delete()

        print("Loading Data")
        call_command('loaddata', fixture_file, verbosity=0)
        print("Awesome. Your data is loaded!")
