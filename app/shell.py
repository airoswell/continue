from app.models import Item, Post
from app.models import ItemEditRecord, PostItemStatus, ItemTransactionRecord
from app.models import PostAndItemsRequest, UserProfile
from django.contrib.auth.models import User
from postman.models import Message
from haystack.query import SearchQuerySet

from app.serializers import ItemSerializer, PostSerializer, UserSerializer
from app.serializers import PostItemStatusSerializer, TransactionSerializer
from app.serializers import UserProfileSerializer

from django.utils.six import BytesIO

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

for item in Item.objects.all():
    if item.previous_owners.all():
        print("\n")
        print(item.title)
        print(item.previous_owners.all())

Item.objects.filter(previous_owners__username='yiwen')
