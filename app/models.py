from django.db import models
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=144, blank=False, null=False)
    quantity = models.IntegerField(default=1)
    condition_choices = (
        ('nw', 'New'),
        ('Ln', 'Like new'),
        ('Gd', 'Good'),
        ('Fl', 'Functional'),
    )
    condition = models.CharField(
        max_length=2,
        choices=condition_choices,
        default='Gd'
    )
    detail = models.TextField(default='')
    link = models.URLField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class RegUser(User):
    nickname = models.CharField(default='', max_length=140)
    to_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='PassEvent',
        through_fields=('giver', 'receiver')
    )

    def __unicode__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=144, blank=False, null=False)
    owner = models.ForeignKey(RegUser)
    item = models.ManyToManyField(
        Item,
        through='ItemStatus',
        through_fields=('post', 'item'),
    )
    zip_code = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        default=''
    )
    detail = models.TextField(default='')
    today = datetime.date.today()
    day = today + relativedelta(months=1)
    expiration_date = models.DateField(default=day)
    time_posted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class PassEvent(models.Model):
    item = models.ForeignKey(Item, related_name='related_events')
    post = models.ForeignKey(Post, related_name='related_events')
    giver = models.ForeignKey(
        RegUser,
        related_name='events_as_giver'
    )
    receiver = models.ForeignKey(
        RegUser,
        related_name='events_as_receiver'
    )
    time_happened = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.item


class ItemStatus(models.Model):
    item = models.ForeignKey(Item, related_name='related_status')
    post = models.ForeignKey(Post, related_name='related_status')
    status_choices = (
        ('av', 'Available'),
        ('po', 'Possed on'),
        ('dp', 'Disposed'),
        ('dl', 'Deleted'),
    )
    item_status = models.CharField(
        max_length=2,
        choices=status_choices,
        default='av',
    )
    item_request = models.ManyToManyField(RegUser)

    def __unicode__(self):
        return self.item.title
