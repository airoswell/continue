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

for profile in UserProfile.objects.all():
    print("user = %s, id = %s" % (profile.user, profile.id))

for item in Item.objects.all():
    print("item %(item)s has owner %(owner)s with id %(owner_id)s" % {"item": item, "owner": item.owner, "owner_id": item.owner.id})

me = User.objects.all()[1]
Post.objects.create(title='\xE4\xB8\xAD\xE6\x96\x87', area="11790", owner=me)