from app.models import Item, Post
from app.models import ItemEditRecord, PostItemStatus, ItemTransactionRecord
from app.models import PostAndItemsRequest, UserProfile, CustomizedCharField
from app.models import Parent, Child
from app.models import CustomizedNumField
from django.contrib.auth.models import User
from postman.models import Message
from haystack.query import SearchQuerySet

from app.serializers import ItemSerializer, PostSerializer, UserSerializer
from app.serializers import PostItemStatusSerializer, TransactionSerializer
from app.serializers import UserProfileSerializer
from app.serializers import ChildSerializer, ParentSerializer

from django.utils.six import BytesIO

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import operator
from django.db.models import Q

parent = Parent.objects.create(title='parent')
son = Child.objects.create(title="son")
daughter = Child.objects.create(title="daughter")
parent = Parent.objects.all()[0]
son = Child.objects.filter(title="son")
daughter = Child.objects.filter(title="daughter")

ai = User.objects.all()[2]
data = {"owner": ai.uid(), "title": "another item"}
s = ItemSerializer(data=data)
s.is_valid()