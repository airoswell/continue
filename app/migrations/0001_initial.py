# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('postman', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=144)),
                ('quantity', models.IntegerField(default=1)),
                ('tags', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('visibility', models.CharField(default=b'Private', max_length=2, choices=[(b'Private', b'Private'), (b'Previous owners', b'Previous owners'), (b'Public', b'Public')])),
                ('condition', models.CharField(default=b'Good', max_length=20, choices=[(b'New', b'New'), (b'Like new', b'Like new'), (b'Good', b'Good'), (b'Functional', b'Functional'), (b'Broken', b'Broken')])),
                ('short_description', models.CharField(default=b'', max_length=140, null=True, blank=True)),
                ('status', models.CharField(default=b'', max_length=140, blank=True)),
                ('detail', models.TextField(default=b'', blank=True)),
                ('intented_use', models.CharField(default=b'', max_length=140, blank=True)),
                ('utilization', models.CharField(default=b'Sometimes', max_length=20, choices=[(b'Frequent', b'Frequent'), (b'Sometimes', b'Sometimes'), (b'Rarely', b'Rarely'), (b'Never', b'Never')])),
                ('availability', models.CharField(default=b'In use', max_length=20, choices=[(b'Available', b'Available'), (b'In use', b'In use'), (b'Lent to someone', b'Lent to someone'), (b'Given away', b'Given away'), (b'Disposed', b'Disposed')])),
                ('acquiring_date', models.DateTimeField(null=True, blank=True)),
                ('original_value', models.IntegerField(null=True, blank=True)),
                ('estimated_value', models.IntegerField(null=True, blank=True)),
                ('link', models.URLField(default=b'', blank=True)),
                ('pic', models.URLField(default=b'', max_length=500, blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('previous_owners', models.ManyToManyField(related_name=b'previously_owned_item', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemEditRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=100)),
                ('original_value', models.CharField(max_length=100)),
                ('new_value', models.CharField(max_length=100)),
                ('note', models.CharField(default=b'', max_length=140)),
                ('time_updated', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(related_name=b'history_event', to='app.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemTransactionRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Sent', max_length=20, choices=[(b'Sent', b'Sent'), (b'Received', b'Received'), (b'Dismissed', b'Dismissed'), (b'Revoked', b'Revoked')])),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('giver', models.ForeignKey(related_name=b'transactions_as_giver', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(related_name=b'related_events', to='app.Item')),
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
                ('tags', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('detail', models.TextField(default=b'', blank=True)),
                ('expiration_date', models.DateField(default=datetime.date(2015, 2, 5))),
                ('time_posted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostAndItemsRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('items', models.ManyToManyField(to='app.Item')),
                ('message', models.ForeignKey(to='postman.Message')),
                ('post', models.ForeignKey(to='app.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostItemStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_status', models.CharField(default=b'Available', max_length=2, choices=[(b'Available', b'Available'), (b'Transfered', b'Transfered'), (b'Disposed', b'Disposed'), (b'Deleted', b'Deleted')])),
                ('item', models.ForeignKey(related_name=b'status_in_post', to='app.Item')),
                ('item_requesters', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(related_name=b'status_in_post', to='app.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(default=b'', null=True, blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(related_name=b'related_reviews', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(related_name=b'related_reviews', to='app.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100, blank=True)),
                ('zip_code', models.CharField(default=b'', max_length=5, blank=True)),
                ('email', models.EmailField(max_length=500, null=True, blank=True)),
                ('social_account_provider', models.CharField(default=b'', max_length=20, blank=True)),
                ('social_account_uid', models.CharField(default=b'', max_length=100, blank=True)),
                ('social_account_url', models.EmailField(max_length=500, null=True, blank=True)),
                ('social_account_photo', models.URLField(default=b'', blank=True)),
                ('user', models.ForeignKey(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='items',
            field=models.ManyToManyField(to='app.Item', through='app.PostItemStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemtransactionrecord',
            name='post',
            field=models.ForeignKey(related_name=b'related_events', to='app.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemtransactionrecord',
            name='receiver',
            field=models.ForeignKey(related_name=b'transactions_as_receiver', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
