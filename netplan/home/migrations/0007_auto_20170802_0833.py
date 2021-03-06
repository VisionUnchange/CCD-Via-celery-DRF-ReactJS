# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 08:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailsearchpromotions', '0002_capitalizeverbose'),
        ('wagtailcore', '0039_collectionviewrestriction'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('home', '0006_auto_20170802_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standardpage',
            name='feed_image',
        ),
        migrations.RemoveField(
            model_name='standardpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='standardpagecarouselitem',
            name='image',
        ),
        migrations.RemoveField(
            model_name='standardpagecarouselitem',
            name='link_document',
        ),
        migrations.RemoveField(
            model_name='standardpagecarouselitem',
            name='link_page',
        ),
        migrations.RemoveField(
            model_name='standardpagecarouselitem',
            name='page',
        ),
        migrations.RemoveField(
            model_name='standardpagerelatedlink',
            name='link_document',
        ),
        migrations.RemoveField(
            model_name='standardpagerelatedlink',
            name='link_page',
        ),
        migrations.RemoveField(
            model_name='standardpagerelatedlink',
            name='page',
        ),
        migrations.DeleteModel(
            name='StandardPage',
        ),
        migrations.DeleteModel(
            name='StandardPageCarouselItem',
        ),
        migrations.DeleteModel(
            name='StandardPageRelatedLink',
        ),
    ]
