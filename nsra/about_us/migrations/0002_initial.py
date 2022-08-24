# Generated by Django 3.2.11 on 2022-08-08 13:26

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('about_us', '0001_initial'),
        ('core_functions', '0001_initial'),
        ('wagtailcore', '0066_collection_management_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutuspagecorefunctionorderable',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_functions.corefunction'),
        ),
        migrations.AddField(
            model_name='aboutuspagecorefunctionorderable',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='functions', to='about_us.aboutuspage'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='functions_cta_link',
            field=models.ForeignKey(blank=True, help_text='Choose a core function index page to link to for the Call to Action(normally some index page)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core_functions.corefunctionindexpage', verbose_name='Core Function Index CTA link'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='hero_cta_link',
            field=models.ForeignKey(blank=True, help_text='Choose a page to link to for the Call to Action', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Hero CTA link'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='hero_image',
            field=models.ForeignKey(blank=True, help_text='Landscape mode only; horizontal width between 1000px and 3000px.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='mandate_icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='mission_icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='og_image',
            field=models.ForeignKey(blank=True, help_text='Shown when linking to this page on social media.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Preview image'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='struct_org_image',
            field=models.ForeignKey(blank=True, help_text='A photo of the facility. This photo will be cropped to 1:1, 4:3, and 16:9 aspect ratios automatically.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Photo of Organization'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='struct_org_logo',
            field=models.ForeignKey(blank=True, help_text='Leave blank to use the logo in Settings > Layout > Logo', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Organization logo'),
        ),
        migrations.AddField(
            model_name='aboutuspage',
            name='vision_icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
