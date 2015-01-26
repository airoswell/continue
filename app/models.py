# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from rest_framework import status as st
from postman.models import Message
from dateutil.relativedelta import relativedelta

from allauth.account.signals import user_logged_in

from django.db.models import Q
import operator
import datetime

# Create your models here.


# ======== Modifying User class ========
def photo(self):
    return self.profile.all()[0].social_account_photo

User.photo = photo


def pending_transactions(self):
    transactions = ItemTransactionRecord.objects.filter(
        (Q(giver=self) | Q(receiver=self)) & Q(status="Sent")
    )
    return transactions


def name(self):
    return self.profile.all()[0].name


def interested_areas(self):
    return self.profile.all()[0].interested_areas


def primary_area(self):
    return self.profile.all()[0].primary_area

User.pending_transactions = pending_transactions
User.interested_areas = interested_areas
User.name = name
User.primary_area = primary_area

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    name = models.CharField(max_length=100, default="", blank=True)
    primary_area = models.CharField(max_length=5, default="", blank=True)
    interested_areas = models.CharField(
        max_length=1000, default="", blank=True)
    email = models.EmailField(
        blank=True, null=True, max_length=500)
    social_account_provider = models.CharField(
        max_length=20, default="", blank=True)
    social_account_uid = models.CharField(
        max_length=100, default="", blank=True
    )
    social_account_url = models.EmailField(blank=True, null=True,
                                           max_length=500)
    social_account_photo = models.URLField(default="", blank=True)
    already_set = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def update(cls, validated_data, **kwargs):
        queryset = cls.objects.filter(id=validated_data['id'])
        if kwargs:  # further filter for permission purpose
            queryset = queryset.filter(**kwargs)
        if not queryset:
            return None, "profile specified by %s not fould." % (kwargs)
        queryset.update(**validated_data)
        profile = queryset[0]
        return profile, []

from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def CreateProfile(sender, **kwargs):
    """
    Populate user profile when user sign up.
    """
    user = kwargs.pop('user')
    email = user.email
    name = user.username
    uid = ""
    social_account_provider = ""
    social_account_photo = "http://siliconangle.com/files/2013/06/20338-anonymous-v-for-vendetta-mask.jpg"
    if user.socialaccount_set.all():
        Provider = user.socialaccount_set.all()[0]
        social_account_provider = Provider.provider
        uid = Provider.uid
        extra_data = Provider.extra_data
        if "email" in extra_data:
            email = extra_data["email"]
        name = extra_data['name']
        social_account_photo = Provider.get_avatar_url()
    UserProfile.objects.create(
        email=email, social_account_uid=uid, name=name, user=user,
        social_account_provider=social_account_provider,
        social_account_photo=social_account_photo)


@receiver(user_logged_in)
def CheckAndUpdateProfile(sender, **kwargs):
    """
    Every time the user logs in, check check and update user's profile
    if the user is registered using a social account.
    """
    user = kwargs['user']
    queryset = UserProfile.objects.filter(user__id=user.id)
    if not queryset:
        CreateProfile(sender, **kwargs)
        return
    profile = queryset[0]
    if user.socialaccount_set.all():
        Provider = user.socialaccount_set.all()[0]
        social_account_provider = user.socialaccount_set.all()[0].provider
        uid = Provider.uid
        # extra_data
        extra_data = Provider.extra_data
        email = None
        if "email" in extra_data:
            email = extra_data["email"]
        name = extra_data['name']
        social_account_photo = Provider.get_avatar_url()
        profile.social_account_provider = social_account_provider
        profile.social_account_photo = social_account_photo
        profile.social_account_uid = uid
        profile.name = name
        profile.email = email if email else ""
        profile.save()
    return


class Item(models.Model):
    title = models.CharField(max_length=144, blank=False)
    owner = models.ForeignKey(User, related_name="inventory")
    area = models.CharField(max_length=5, default="", blank=True)
    area_descripttion = models.CharField(
        max_length=500, default="", blank=True,
    )
    requesters = models.ManyToManyField(User, related_name="items_requested")
    quantity = models.IntegerField(default=1)
    model = models.CharField(max_length=200, default="", blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True, default="")
    tags_private = models.CharField(
        max_length=500, blank=True, null=True, default=""
    )
    size = models.CharField(
        max_length=100,
        default="Small", blank=True
    )
    visibility_choices = (
        ('Private', "Private"),
        ('Ex-owners', "Ex-owners"),
        ('Public', "Public")
    )
    visibility = models.CharField(
        choices=visibility_choices,
        max_length=10,
        default="Private",
    )
    condition_choices = (
        ("Inapplicable", "Inapplicable"),
        ('New', 'New'),
        ('Like new', 'Like new'),
        ('Good', 'Good'),
        ('Functional', 'Functional'),
        ('Broken', 'Broken'),
    )
    condition = models.CharField(
        max_length=20,
        choices=condition_choices,
        default='Good'
    )
    transferrable = models.BooleanField(default=True)
    available_choices = (
        ("For Share", "For Share"), ("For Sale", "For Sale"), ("No", "No")
    )
    available = models.CharField(
        choices=available_choices,
        default="No",
        max_length=20,
    )
    previous_owners = models.ManyToManyField(
        User,
        related_name='previously_owned_item',
    )
    description = models.CharField(
        max_length=140, default="", blank=True, null=True
    )
    status = models.CharField(max_length=300, default="", blank=True)
    detail = models.TextField(default='', blank=True)
    intented_use = models.CharField(max_length=140, default="", blank=True)
    utilization_choices = (
        ("Inapplicable", "Inapplicable"),
        ("Daily", "Daily"),
        ('Frequent', 'Frequent'),
        ('Sometimes', 'Sometimes'),
        ('Rarely', 'Rarely'),
        ('Never', 'Never'),
    )
    utilization = models.CharField(
        max_length=20,
        choices=utilization_choices,
        default='Sometimes',
    )
    availability_choices = (
        ('Available', 'Available'),
        ('In use', 'In use'),
        ('Lent', 'Lent'),
        ('Given away', 'Given away'),
        ('Disposed', 'Disposed'),
    )
    availability = models.CharField(
        max_length=20,
        choices=availability_choices,
        default='In use'
    )
    acquiring_date = models.DateTimeField(blank=True, null=True)
    original_value = models.IntegerField(blank=True, null=True)
    estimated_value = models.IntegerField(blank=True, null=True)
    link = models.URLField(default='', blank=True)
    pic = models.URLField(max_length=500, default='', blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

    def __unicode__(self):
        return unicode(self.title)

    def model_name(self):
        return type(self).__name__

    def owner_profile(self):
        return {
            "name": self.owner.name(),
            "photo": self.owner.photo(),
        }

    @property
    def tracked_fields(self):
        return ('owner', 'status',
                'condition', 'utilization', 'availability',
                'estimated_value', 'pic',
                "description", )

    @classmethod
    def create(cls, validated_data, *args, **kwargs):
        """
        Item.create()
        """
        # Typically validated_data should be feed with empty
        # customized_num/char_fields, when they are not specified.
        if "customized_num_fields" in validated_data:
            num_fields_data = validated_data.pop('customized_num_fields')
        if "customized_char_fields" in validated_data:
            char_fields_data = validated_data.pop('customized_char_fields')
        print("\n\tItem.create() ==> validated_data = %s" % (validated_data))
        item = cls.objects.create(**validated_data)
        ItemEditRecord.objects.create(
            item=item, field="creation",
            original_value="", new_value=""
        )
        item.save()
        for data in num_fields_data:
            data['item'] = item
            field = CustomizedNumField.objects.create(
                **data
            )
            print(field)
        return item

    @classmethod
    def update(cls, validated_data, **kwargs):
        """ Item.update()
        Update using <update, method of Queryset>.
        """
        queryset = cls.objects.filter(id=validated_data["id"])
        # kwargs can contain [owner=request.user] to impose
        # permission check
        if kwargs:
            queryset = queryset.filter(**kwargs)
        if not queryset:
            # Deal with the case where the item is not found
            return None, []
        customized_num_fields_data = []
        customized_char_fields_data = []
        if 'customized_num_fields' in validated_data:
            customized_num_fields_data = validated_data.pop(
                'customized_num_fields'
            )
        if "customized_char_fields" in validated_data:
            customized_char_fields_data = validated_data.pop(
                'customized_char_fields'
            )
        item = queryset[0]
        owner_changed = False
        errors = []
        item.update_customized_fields(
            CustomizedNumField, customized_num_fields_data
        )
        item.update_customized_fields(
            CustomizedCharField, customized_char_fields_data
        )
        for field in item.tracked_fields:
            print("\t\tfield = %s" % (field))
            if not (field in validated_data):
                continue
            original_value = getattr(item, field)
            new_value = validated_data[field]
            if new_value != original_value:
                # If:
                # - there is ownership change
                # - and the item is currently transferrable
                # create a new transaction
                if field == "owner" and item.transferrable:
                    ItemTransactionRecord.objects.create(
                        item=item,
                        giver=original_value,    # the current owner
                        receiver=new_value,
                        status="Sent",
                    )
                    # Do not perform the change of ownership right now
                    # Wait for the confirmation of the other side.
                    # - The transfer itself should be done in the
                    # <TransactionRecord> model by a PUT request.
                    validated_data.pop("owner")
                    owner_changed = True
                else:
                    record = ItemEditRecord(
                        item=item, field=field,
                        original_value=original_value,
                        new_value=new_value,
                    )
                    from django.db import IntegrityError
                    try:
                        record.save()
                    except IntegrityError, e:
                        errors.push(e.message)
                        errors.push(field)
                        errors.push(original_value)
                        errors.push(new_value)
                        print("\n\tItem.update: errors %s" % (errors))
        # Owner change will propagate through here
        print("\t\t Item.update: validated_data %s" % (validated_data))
        try:
            queryset.update(**validated_data)
        except FieldError, e:
            print("\t\t %s" % ("!*"*10))
            print("\t\nItem.update: FieldError: %s " % (e.message))
            print("\t\t %s" % ("!*"*10))
            return queryset[0], [e.message]
        # A newly created transaction should render the item NOT-transferrable
        if owner_changed:
            queryset.update(transferrable=False)
        queryset[0].save()      # To trigger Haystack update_index
        print("\t\t Item.update() ==> errors: %s" % (errors))
        return queryset[0], errors

    def update_customized_fields(self, model, customized_fields_data):
        for field_data in customized_fields_data:
            field_data["item"] = self
            try:
                # Get the old value and update/create the field
                if 'id' in field_data:
                    qs = model.objects.filter(pk=field_data['id'])
                    if not qs:
                        pass
                    existing_field = qs[0]
                    old_value = existing_field.value
                    qs.update(**field_data)
                else:
                    old_value = None
                    model.objects.create(
                        **field_data
                    )
                # Extract the new_value
                if "unit" in field_data:
                    new_value = "%s %s" % (
                        field_data['value'], field_data['unit']
                    )
                else:
                    new_value = field_data['value']
                print("\n\told_value = %s, new_value = %s" % (old_value, new_value))
                if old_value != new_value:
                    ItemEditRecord.objects.create(
                        field=field_data['title'],
                        original_value=old_value,
                        new_value=new_value,
                        item=self,
                    )
            except:
                print("item.update_customized_char_fields error")
        return


class CustomizedCharField(models.Model):
    item = models.ForeignKey(Item, related_name="customized_char_fields")
    title = models.CharField(max_length=144, blank=False)
    value = models.CharField(max_length=500, blank=True, default="")
    time_updated = models.DateTimeField(auto_now=True)
    time_created = models.DateTimeField(auto_now_add=True)


class CustomizedNumField(models.Model):
    item = models.ForeignKey(Item, related_name="customized_num_fields")
    title = models.CharField(max_length=144, blank=False)
    value = models.DecimalField(max_digits=10, decimal_places=3, blank=False)
    unit = models.CharField(max_length=20, blank=True, default="")
    time_updated = models.DateTimeField(auto_now=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=144, blank=False)
    owner = models.ForeignKey(User)
    items = models.ManyToManyField(
        Item,
        through='PostItemStatus',
        through_fields=('post', 'item'),
    )
    area = models.CharField(
        max_length=5,
        blank=False,
        default='',
    )
    tags = models.CharField(max_length=500, blank=True, null=True, default="")
    detail = models.TextField(default='', blank=True)
    visibility_choices = (
        ('Private', 'Private'),
        ('Public', 'Public'),
        ('Invitation', 'Invitation'),
    )
    visibility = models.CharField(
        max_length=20, blank=False,
        choices=visibility_choices,
        default='Public'
    )
    secret_key = models.CharField(
        max_length=100, blank=True, default=''
    )
    today = datetime.date.today()
    day = today + relativedelta(months=1)
    expiration_date = models.DateField(default=day)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

    def remaining_time(self):
        from datetime import datetime
        now = datetime.now()
        if self.expiration_date:
            exp = self.expiration_date
            exp = datetime.combine(exp, datetime.min.time())
            d = exp - now
            return d.days
        else:
            return None

    @classmethod
    def update(cls, validated_data, **kwargs):
        print("\t\nPost.update() begins..\n")
        items_data = None
        if "items" in validated_data:
            items_data = validated_data.pop("items")
        post_data = validated_data
        queryset = Post.objects.filter(id=validated_data['id'])
        # Further restrict the queryset
        # typically used for confirming the ownership
        errors = []
        if kwargs:
            queryset = queryset.filter(**kwargs)
        if queryset.update(**post_data) == 0:
            return None, ["Updated zero posts."]
        post = queryset[0]
        if items_data is None:
            return post, errors
        current_item_list = [item.id for item in post.items.all()]
        for item_data in items_data:
            # Items that are already in the database
            if "id" in item_data:
                try:
                    # Update existing items that were already in the post
                    if item_data['id'] in current_item_list:
                        item, item_errors = Item.update(item_data, **kwargs)
                    # Update existing items that were not in the post
                    else:
                        item, item_errors = Item.update(item_data, **kwargs)
                        PostItemStatus.objects.create(
                            post=post,
                            item=Item.objects.get(id=item_data['id'])
                        )
                    errors.append(item_errors)
                # ====================================================
                # If the item is not found in the database, just pass,
                # might change in the future to throw an error
                except Item.DoesNotExist, e:
                    errors.append(e.message)
                    pass
            else:       # Items that are brand new
                post.add_item(item_data)
        post.save()     # To trigger Haystack to run update_index
        return post, errors

    def add_item(self, validated_item_data):
        item = Item.create(validated_item_data)
        PostItemStatus.objects.create(
            item=item, post=self,
        )
        return True

    @classmethod
    def create(cls, validated_data, *args, **kwargs):
        """
        Post.create()
        """
        items_data = None
        if "items" in validated_data:
            items_data = validated_data.pop("items")
        post_data = validated_data
        post = cls.objects.create(**post_data)
        print("\t\tvalidated_data = %s" % (validated_data))
        if items_data:
            for item_data in items_data:
                if not "id" in item_data:
                    item = Item.create(item_data)
                else:
                    item, errors = Item.update(item_data)
                PostItemStatus.objects.create(
                    item=item, post=post,
                )
        post.save()         # trigger update_index
        return post

    @classmethod
    def in_areas(cls, *areas):
        """
        <areas> should be a list of zip_codes, and in_areas will return
        all posts in either of the areas.
        Can be used for searching posts from multiple areas
        """

        return (cls.objects.filter(area__in=list(areas))
                .order_by("-time_created"))

    def owner_photo(self):
        return self.owner.photo()

    def owner_name(self):
        return self.owner.name()

    def model_name(self):
        return type(self).__name__

    def __unicode__(self):
        return unicode(self.title)


class Review(models.Model):
    item = models.ForeignKey(Item, related_name="related_reviews")
    author = models.ForeignKey(User, related_name='related_reviews')
    body = models.TextField(default="", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

    def __unicode__(self):
        return unicode(self.item)


class ItemTransactionRecord(models.Model):
    item = models.ForeignKey(Item, related_name='transaction_records')
    giver = models.ForeignKey(
        User,
        related_name='transactions_as_giver'
    )
    receiver = models.ForeignKey(
        User,
        related_name='transactions_as_receiver'
    )
    status_choices = (
        ('Sent', 'Sent'),
        ('Received', 'Received'),
        ('Dismissed', 'Dismissed'),
        ('Revoked', 'Revoked'),
    )
    status = models.CharField(
        max_length=20, default='Sent',
        choices=status_choices
    )
    time_updated = models.DateTimeField(auto_now=True)
    time_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-status', '-time_updated']

    @classmethod
    def update(cls, validated_data, **kwargs):
        queryset = cls.objects.filter(pk=validated_data['id'])
        if queryset:
            transaction = queryset[0]
            # For status == "Dismissed", "Received", "Revoked"
            # no action should be taken
            if transaction.status != "Sent":
                return transaction, []
            new_status = validated_data['status']
            item = validated_data['item']
            giver = validated_data['giver']
            receiver = validated_data["receiver"]
            transaction.status = new_status
            if new_status == "Received":
                item.owner = receiver
                item.visibility = "Ex-owners"
                # Add original owner to the previous_owners field
                item.previous_owners.add(giver)
                # Clear previous requesters
                for requester in item.requesters.all():
                    item.requesters.remove(requester)
            # If the item is revoked, the requester should be able
            # to request it again, thus remove him/her from the
            # requester list.
            if new_status == "Revoked":
                item.requesters.remove(receiver)
            item.transferrable = True
            item.save()
            transaction.save()
        return transaction, []

    def model_name(self):
        return type(self).__name__

    def __unicode__(self):
        return unicode(self.item)


class PostItemStatus(models.Model):
    item = models.ForeignKey(Item, related_name='status_in_post')
    post = models.ForeignKey(Post, related_name='status_in_post')
    item_requesters = models.ManyToManyField(User)

    def __unicode__(self):
        return unicode(self.item.title)


class ItemEditRecord(models.Model):
    item = models.ForeignKey(Item, related_name='history_event')
    field = models.CharField(max_length=100)
    original_value = models.CharField(max_length=500, blank=True, null=True)
    new_value = models.CharField(max_length=500)
    note = models.CharField(max_length=500, default="", blank=True, null=True)
    time_updated = models.DateTimeField(auto_now_add=True)

    def model_name(self):
        return type(self).__name__

    def __unicode__(self):
        return unicode(self.item)


class PostAndItemsRequest(models.Model):
    post = models.ForeignKey(Post)
    items = models.ManyToManyField(Item)
    message = models.ForeignKey(Message, related_name='request')

    def __unicode__(self):
        return unicode(self.message)


class Image(models.Model):
    image = models.ImageField(upload_to='item_images')
    owner = models.ForeignKey(
        User, related_name='uploaded_item_images',
        blank=False,
    )
    time_created = models.DateTimeField(auto_now_add=True)
