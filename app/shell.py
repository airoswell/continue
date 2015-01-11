from app.models import Item, Post
from app.models import ItemEditRecord, PostItemStatus, ItemTransactionRecord
from app.models import PostAndItemsRequest, UserProfile
from django.contrib.auth.models import User
from postman.models import Message
from haystack.query import SearchQuerySet

from app.serializers import ItemSerializer, PostSerializer, UserSerializer
from app.serializers import PostItemStatusSerializer, TransactionSerializer
from app.serializers import ProfileSerializer

from django.utils.six import BytesIO

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

item = Item.objects.filter(title__icontains="Apple wireless")[0]

records = item.history_event.all()

ItemEditRecord.objects.filter(item=item)
