# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('url', models.URLField()),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d')),
                ('description', models.TextField(blank=True)),
                ('created', models.DateField(db_index=True, auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='images_created')),
                ('user_like', models.ManyToManyField(blank=True, related_name='images_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
