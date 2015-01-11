# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_auto_20150107_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='requesters',
            field=models.ManyToManyField(related_name='items_requested', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(related_name='inventory', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
