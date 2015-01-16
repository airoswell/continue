# -*- coding: utf-8 -*-
from app.models import Item, Post, UserProfile
from app.models import ItemEditRecord, PostItemStatus, ItemTransactionRecord
from django.contrib.auth.models import User
from postman.models import Message

from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("id", "name", "social_account_photo", "email",
                  "primary_area", "interested_areas", "already_set", )


class UserSerializer(serializers.ModelSerializer):

    # expect to have several profiles in rare cases
    profile = UserProfileSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', "profile")


class ItemSerializer(serializers.ModelSerializer):
    requesters = UserSerializer(many=True, read_only=True)
    transferrable = serializers.BooleanField(read_only=True)

    def as_instance(self):
        return Item.objects.get(pk=self.data['id'])

    class Meta:
        model = Item
        fields = ("id", "title",
                  "quantity", "condition", "description", "model",
                  "visibility", "detail", 'status', "utilization",
                  "availability", "link", "pic", "time_created", 'owner',
                  "acquiring_date", "original_value", "estimated_value",
                  "requesters", "transferrable", "tags", "tags_private",
                  "previous_owners", 'model_name', 'owner_profile',
                  )
        read_only_fields = ('previous_owners', "time_created", "requesters",
                            "owner_profile")


class ItemSerializerLite(serializers.ModelSerializer):
    """
    A lite version of ItemSerializer, only serialize basic information about
    an item, used for items in post.
    """

    def create(self, validated_data):
        # Return a list of Item instance when serializing with (many=True)
        # Return a single Item instance when only one
        return Item.objects.create(**validated_data)

    def as_instance(self):
        return Item.objects.get(pk=self.data['id'])

    class Meta:
        model = Item
        fields = ("id", "title", "quantity", "condition",
                  "description", "availability", "tags", 'model_name')


class PostSerializer(serializers.ModelSerializer):
    """
    Capable of fully serialize <Post> (with full fledge items information).
    Typically use for user dashboard editing, where full info about
    sub items are needed, while the owner of the posts is not necessary
    and can be simplified (just use the <id>).
    """
    items = ItemSerializer(many=True, read_only=True)

    @classmethod
    def create(self, validated_data):
        """
        Create the post with items.
        - Items that are brand new, run Item.create(validated_data)
        - Items that are already in the database, run update
        """
        return Post.objects.create(**validated_data)

    def as_instance(self):
        return Post.objects.get(pk=self.validated_data['id'])

    def full_serialization(self):
        owner = User.objects.get(id=self.data["owner"])
        owner_data = UserSerializer(owner).data
        data = self.data
        data['owner'] = owner_data
        return data

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'area', 'detail',
                  'time_posted', 'expiration_date', 'items', "tags",
                  'remaining_time', 'owner_photo', 'owner_name', "model_name",
                  )


class PostSerializerLite(serializers.ModelSerializer):
    items = ItemSerializerLite(many=True, read_only=True)
    owner = UserSerializer()

    def as_instance(self):
        return Post.objects.get(pk=self.validated_data['id'])

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'area', 'detail',
                  'time_posted', 'expiration_date', 'items', 'owner', "tags",
                  'remaining_time', 'model_name',
                  )


class PostItemStatusSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    post = PostSerializer()
    item_requesters = UserSerializer(many=True)

    def as_instance(self):
        return PostItemStatus.objects.get(pk=self.validated_data['id'])

    class Meta:
        model = PostItemStatus
        fields = ('item', 'post', 'item_status', 'item_requesters')


class ItemEditRecordSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = ItemEditRecord
        fields = ('id', 'item', 'field',
                  'original_value', 'new_value', 'time_updated', 'model_name')


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('sender', 'recipient', 'subject', 'body', 'sent_at')


class TransactionSerializer(serializers.ModelSerializer):
    item = ItemSerializerLite()
    giver = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = ItemTransactionRecord
        fields = ("id", "item", "giver", "receiver", "status",
                  "time_updated", "time_sent")


class TransactionSerializerLite(serializers.ModelSerializer):
    # Remove UserSerializer to easily manipulate owners:
    # using <pk>, the serializer can turn <pk> into user instance
    # while using {"username": "...", id: ..} one cannot serialize it
    # into a user instance

    class Meta:
        model = ItemTransactionRecord
        fields = ("id", "item", "giver", "receiver", "status",
                  "time_updated", "time_sent")
