from django.db import models
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta
import pdb

# Create your models here.


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


class Item(models.Model):
    title = models.CharField(max_length=144, blank=False, null=False)
    current_owner = models.ForeignKey(RegUser, null=True)
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
    short_description = models.CharField(max_length=140, blank=True, null=True)
    detail = models.TextField(default='')
    utilization_choices = (
        ('fr', 'Frequent'),
        ('st', 'Sometimes'),
        ('rr', 'Rare'),
        ('nv', 'Never'),
    )
    utilization = models.CharField(
        max_length=2,
        choices=utilization_choices,
        default='st',
    )
    availability_choices = (
        ('av', 'Available'),
        ('iu', 'In use'),
        ('hd', 'Hidden')
    )
    availability = models.CharField(
        max_length=2,
        choices=availability_choices,
        default='hd'
    )
    link = models.URLField(default='')
    time_created = models.DateTimeField(auto_now_add=True)

    def has_owner(self):
        if self.current_owner.id:
            return True
        return False

    def __unicode__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=144, blank=False, null=False)
    owner = models.ForeignKey(RegUser)
    item = models.ManyToManyField(
        Item,
        through='ItemPostRelation',
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

    def some_method(self):
        return self

    def add_item(self, item_data):
        owner = RegUser.objects.get(id=item_data['owner_id'])
        # pdb.set_trace()
        item = Item(
            title=item_data['title'],
            current_owner=owner,
            quantity=item_data['quantity'],
            condition=item_data['condition'],
            detail=item_data['detail'],
            link=item_data['link'],
        )
        # pdb.set_trace()
        item.save()
        ItemPostRelation.objects.create(
            item=item,
            post=self,
        )
        return True

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


class ItemPostRelation(models.Model):
    item = models.ForeignKey(Item, related_name='related_status')
    post = models.ForeignKey(Post, related_name='related_status')
    status_choices = (
        ('av', 'Available'),
        ('po', 'Passed on'),
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
