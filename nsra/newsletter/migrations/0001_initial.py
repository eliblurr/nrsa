# Generated by Django 3.2.11 on 2022-08-08 13:26

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('birdsong', '0005_alter_receipt_success'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('campaign_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='birdsong.campaign')),
                ('headline', models.CharField(blank=True, help_text='The headline to use for the newsletter.', max_length=255, null=True)),
                ('body', wagtail.core.fields.StreamField([('rich_text', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'bold', 'italic', 'link', 'ul', 'ol', 'document-link'], template='birdsong/mail/blocks/richtext.html'))], null=True, verbose_name='email body content block')),
                ('header_background', models.ForeignKey(blank=True, help_text='The image to use for the header backgound.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            bases=('birdsong.campaign',),
        ),
    ]
