# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=144)),
                ('quantity', models.IntegerField(default=1)),
                ('condition', models.CharField(default=b'Gd', max_length=2, choices=[(b'Ln', b'Like new'), (b'Gd', b'Good'), (b'Fr', b'Fair')])),
                ('detail', models.TextField(default=b'')),
                ('link', models.URLField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_status', models.CharField(default=b'av', max_length=2, choices=[(b'av', b'Available'), (b'po', b'Possed on'), (b'dp', b'Disposed'), (b'dl', b'Deleted')])),
                ('item', models.ForeignKey(related_name=b'related_status', to='app.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PassEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_happened', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=144)),
                ('zip_code', models.CharField(default=b'', max_length=5)),
                ('detail', models.TextField(default=b'')),
                ('expiration_date', models.DateField(default=datetime.date(2014, 11, 25))),
                ('time_posted', models.DateTimeField(auto_now_add=True)),
                ('item', models.ManyToManyField(to='app.Item', through='app.ItemStatus')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=200)),
                ('to_users', models.ManyToManyField(to='app.RegUser', through='app.PassEvent')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(to='app.RegUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passevent',
            name='giver',
            field=models.ForeignKey(related_name=b'events_as_giver', to='app.RegUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passevent',
            name='item',
            field=models.ForeignKey(related_name=b'related_events', to='app.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passevent',
            name='post',
            field=models.ForeignKey(related_name=b'related_events', to='app.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passevent',
            name='receiver',
            field=models.ForeignKey(related_name=b'events_as_receiver', to='app.RegUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemstatus',
            name='item_request',
            field=models.ManyToManyField(to='app.RegUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemstatus',
            name='post',
            field=models.ForeignKey(related_name=b'related_status', to='app.Post'),
            preserve_default=True,
        ),
    ]
