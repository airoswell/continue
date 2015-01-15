# -*- coding: utf-8 -*-
# Models and serializers
from app.models import Item, Post, UserProfile
from app.models import ItemEditRecord, ItemTransactionRecord, PostItemStatus
from app.serializers import *
import app.permissions as perms
from app.errors import *
from GenericAPI import *
from app.CRUD import *
# Django Core
# Django Rest Framework
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework import permissions
# ================================
# Django Allauth
from allauth.socialaccount.models import SocialToken
# Other Python module
from controllers import *


class test(XListAPIView):

    def get(self, request):
        return Response(data=request.query_params)


class PostList(XListAPIView):
    """
        get, create posts of the current user.
    """
    permission_classes = (
        # only logged in user can post
        permissions.IsAuthenticatedOrReadOnly,
    )

    model = Post
    serializer = PostSerializer
    num_of_records = 10

    def get(self, request, format=None):
        self.get_object()
        params = request.query_params
        start, num_of_records = self.paginator(request)
        print "start = %s." % (start)
        if "q" in params:
            s = S(Post)
            s.config(
                num_of_records=num_of_records,
                start=start,
            )
            posts = s.search(params)
            if posts:
                return Response(
                    data=self.serializer(posts, many=True).data,
                )
            else:
                return Response(status=st.HTTP_404_NOT_FOUND)
        # Display list of posts of a specified user
        elif "user_id" in params:
            return run_and_respond(
                retrieve_records,
                Post, PostSerializerLite,
                start, num_of_records,
                owner__id=params["user_id"]
            )
        # Display list of posts of a location
        elif "area" in params:
            return run_and_respond(
                retrieve_records,
                Post, PostSerializerLite,
                start, num_of_records,
                area=params['area']
            )
        # Display all posts of the current user
        data, status = retrieve_records(
            Post, PostSerializer,
            start, num_of_records,
            owner__id=request.user.id
        )
        return Response(data=data, status=status)

    def post(self, request, format=None):
        """
        PostList.post
        """
        self.get_object()       # For permissions purpose.
        # Parse the <MergeDict> data
        data = self.parser(request)
        data['owner'] = request.user.id
        # ============================================================
        # First process and validate and rearrange the data
        items_data = []
        items_errors = []
        if "items" in data:
            for item_data in data.pop("items"):
                if not "owner" in item_data:
                    item_data["owner"] = request.user.id
                # if the item belongs to some one else
                # do not proceed. This happens when a posted item is
                # transferred.
                elif item_data['owner'] != request.user.id:
                    continue
                item_id = item_data['id'] if "id" in item_data else None
                item_error_handler = ErrorHandler(ItemSerializer)
                item_data = item_error_handler.validate(item_data)
                # Force the item to be public viewable.
                item_data['visibility'] = "Public"
                if item_error_handler.errors:
                    items_errors.append(item_error_handler.errors)
                if item_id:
                    item_data['id'] = item_id       # Recover the id
                items_data.append(item_data)
        post_error_handler = ErrorHandler(PostSerializer)
        data = post_error_handler.validate(data)
        post_data_errors = post_error_handler.errors
        if items_data:
            data['items'] = items_data
        errors = post_data_errors
        errors['items_errors'] = items_errors
        if "fatal" in errors or "fatal" in errors["items_errors"]:
            return Response(data=errors, status=st.HTTP_400_BAD_REQUEST)
        # ==== Validation END ========================================
        # ============================================================
        # <data> is now validated, should cause minimal problems later
        crud = Crud(request.user, Post)
        post = crud.create(data)
        status = crud.status
        return Response(data=PostSerializer(post).data, status=status)


class PostDetail(XDetailAPIView):

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        perms.IsOwnerOrReadOnly,
    )

    model = Post
    serializer = PostSerializer

    def put(self, request, pk, format=None):
        """
        Update <Post> record, including all related items
        """
        print("\tPostDetail.put ========>")
        # ============================================================
        # First process and validate and rearrange the data
        # - validate all data using serializers
        post_error_handler = ErrorHandler(PostSerializer)
        # - 1. Extract valid post data
        if "id" in request.data:
            post_id = request.data['id']
        data = post_error_handler.validate(request.data)
        data['id'] = post_id
        post_data_errors = post_error_handler.errors
        # - 2. Extract valid items data
        if "items" in request.data:
            items_data = []
            items_errors = []
            for item_data in request.data.pop("items"):
                if not "owner" in item_data:
                    item_data["owner"] = request.user.id
                elif item_data['owner'] != request.user.id:
                    # if the item belongs to some one else
                    # do not proceed
                    continue
                # Store the id,
                # as serializers will remove any existing id
                item_id = item_data['id'] if "id" in item_data else None
                item_error_handler = ErrorHandler(ItemSerializer)
                item_data = item_error_handler.validate(item_data)
                if item_error_handler.errors:
                    items_errors.append(item_error_handler.errors)
                if item_id:
                    item_data['id'] = item_id       # Recover the id
                items_data.append(item_data)
            data['items'] = items_data
        errors = post_data_errors
        errors['items_errors'] = items_errors
        if "fatal" in errors or "fatal" in errors["items_errors"]:
            return Response(data=errors, status=st.HTTP_400_BAD_REQUEST)
        # Validation End
        # ============================================================
        post, status = self.get_object(pk=pk)
        if post:
            crud = Crud(request.user, Post)
            # Pass in keyword argument owner=request.user
            # will further authenticate user at the model.update() level
            post, errors = crud.update(data, owner=request.user)
            data = self.serializer(post).data
            data["errors"] = errors
            return Response(data=data, status=status)
        if not post:
            return Response(
                data='Post not found.',
                status=st.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk, format=None):
        data, status = self.get_object(pk=pk)
        if data:
            data.delete()
            return Response(data="Deleted.", status=st.HTTP_204_NO_CONTENT)
        else:
            return Response(data=[], status=st.HTTP_404_NOT_FOUND)


class ItemList(XListAPIView):
    """
        Create an <item, Item>, or retrieve list of items
    """
    model = Item
    serializer = ItemSerializer
    num_of_records = 20

    def get(self, request, post_id=None, format=None):
        start, num_of_records = self.paginator(request)
        # get list of items owned by a specific user
        # Don't need any authentication
        if request.GET.get("user_id"):
            return run_and_respond(
                retrieve_records,
                Item, ItemSerializer,
                start, num_of_records,
                owner__id=request.GET.get("user_id"),
                visibility="Public",
            )
        # For accessing items of a post
        # No authentication required
        elif post_id:
            return run_and_respond(
                retrieve_records,
                Item, ItemSerializer,
                start, num_of_records,
                status_in_post__post__id=post_id,
            )
        # get list of items of the current authenticated user
        elif not request.user.is_anonymous():
            return run_and_respond(
                retrieve_records,
                Item, ItemSerializer,
                start, num_of_records,
                owner__id=request.user.id,
            )
        # unauthenticated user cannot get any item list
        else:
            return Response(
                status=st.HTTP_401_UNAUTHORIZED,
                data={"error_message": "Please log in."}
            )

    def post(self, request, format=None):
        """
        ItemList.post
        """
        data = self.parser(request)
        # Make sure owner present and correct
        data['owner'] = request.user.id
        handler = ErrorHandler(ItemSerializer)
        data = handler.validate(data)
        if not request.user.is_anonymous():
            crud = Crud(request.user, Item)
            item = crud.create(data)
            data = ItemSerializer(item).data
            data["errors"] = handler.errors
            return Response(data=data, status=crud.status)
        return Response(
            status=st.HTTP_401_UNAUTHORIZED,
            data={"error": "Log in first."}
        )


class ItemDetail(XDetailAPIView):
    '''
        R, U, D of a given <item, Item>
    '''
    permission_classes = (
        perms.IsOwnerOrPublicOrNoPermission,
    )

    model = Item
    serializer = ItemSerializer

    def put(self, request, pk, format=None):
        if "remove_from_post" in request.data:
            post = Post.objects.get(id=request.data['remove_from_post'])
            item = Item.objects.get(id=request.data['id'])
            status = PostItemStatus.objects.get(item=item, post=post)
            status.delete()
        return super(ItemDetail, self).put(request, pk, format=None)


class UserDetails(XDetailAPIView):

    permission_classes = (
        perms.IsSelfOrNoPermission,
        # permissions.IsAuthenticated
    )

    model = UserProfile
    serializer = UserProfileSerializer

    def get(self, request, pk=None):
        if request.user.is_anonymous():
            return Response(
                data=[{"is_anonymous": True}], status=st.HTTP_200_OK)
        profile = None
        from django.core.exceptions import MultipleObjectsReturned
        # In case multiple user profiles were created,
        # choose the latest one
        user = request.user
        try:
            profile = UserProfile.objects.get(user__id=user.id)
        except AssertionError:
            profile = (UserProfile.objects.filter(user__id=user.id)
                                  .order_by('time_created')[0])
        except MultipleObjectsReturned:
            profile = (UserProfile.objects.filter(user__id=user.id)
                                  .order_by('time_created')[0])
        if profile:
            data = self.serializer(profile).data
            data['user_id'] = request.user.id
            data["is_anonymous"] = user.is_anonymous()
            if user.socialaccount_set.all():
                provider = user.socialaccount_set.all()[0]
                data['access_token'] = SocialToken.objects.filter(
                    account__user=user,
                    account__provider=provider.provider
                )[0].token
            return Response(data=[data], status=st.HTTP_200_OK)
        else:
            return Response(status=st.HTTP_404_NOT_FOUND)


from haystack.query import SearchQuerySet


class S:
    def __init__(self, model):
        self.model = model
        self.start = 0
        self.num_of_records = 10

    def config(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def search(self, params):
        start = self.start
        end = self.start + self.num_of_records
        area = ""
        if "area" in params:
            area = params['area']
        if not ("q" in params) and area:
            return self.model.in_areas(area)[start:end]
        # Note that the default ordering of models are not respected here
        if params["q"] != "":
            sqs = (SearchQuerySet().models(Post).filter(content=params['q'])
                   .order_by("-time_posted"))
        # If no parameter is specified, make a full data search
        else:
            sqs = (SearchQuerySet().models(Post).all()
                   .order_by("-time_posted"))
        if area != "":
            sqs = sqs.filter(area=area)
        results = [sq.object for sq in sqs][start:end]
        return results


class SearchPosts(XListAPIView):

    def get(self, request):
        params = request.query_params
        s = S(Post)
        posts = s.search(params)
        data = PostSerializer(posts, many=True).data
        return Response(data=data, status=st.HTTP_200_OK)


from pmAPI import pm_write
from app.models import PostAndItemsRequest
from postman.models import Message
from serializers import MessageSerializer


class MessageList(XListAPIView):

    def get(self, request):
        messages = Message.objects.filter(recipient=request.user)
        return Response(
            data=MessageSerializer(messages, many=True).data,
            status=st.HTTP_200_OK
        )

    def post(self, request):
        # Preprocessing the data
        data = self.parser(request)
        items = []      # to hold item instances
        sender = None
        # Anonymous senders can use their email
        # But this should not go in to serializer
        # since it expects a <User> instance.
        user = request.user
        if user.is_anonymous():
            sender = data['email']
            data.pop("sender")
        if "post_id" in data:
            post = Post.objects.filter(id=data['post_id'])
            if post and ("items" in data):
                post = post[0]
                for item_id in data['items']:
                    item = Item.objects.filter(id=item_id)
                    if item:
                        item = item[0]
                        items.append(item)
                data.pop("items")
            data.pop("post_id")
        # filter and reassemble the data
        handler = ErrorHandler(MessageSerializer)
        message_data = handler.validate(data)
        if handler.errors:
            return Response(
                data=handler.errors, status=st.HTTP_400_BAD_REQUEST
            )
        body = message_data['body']
        subject = message_data['subject']
        recipient = message_data['recipient']
        if not sender:
            sender = message_data['sender']
        # Write to the database
        # when sender = '<email address>', the resulting message
        # will have message.sender = None, message.email = "<address>".
        message = pm_write(
            sender, recipient, subject, body,
        )
        if post:
            req = PostAndItemsRequest.objects.create(
                post=post, message=message
            )
            req.save()
            req.items.add(*items)   # items is an array of item instances
            for item in items:
                status = item.status_in_post.filter(post=post)[0]
                # Add the requester to the item.requesters
                if not (user in status.item_requesters.all()):
                    status.item_requesters.add(request.user)
                if not (user in item.requesters.all()):
                    item.requesters.add(request.user)
        return Response(status=st.HTTP_200_OK)


class HistoryList(XListAPIView):

    model = ItemEditRecord
    serializer = ItemEditRecordSerializer
    num_of_records = 20

    permission_classes = (perms.IsOwnerOrNoPermission,)

    def get(self, request, pk=None, item_id=None):
        start, num_of_records = self.paginator(request)
        if request.user.is_anonymous():
            return Response(
                data={"error": "Unauthorized",
                      "error_detail": "Please log in."},
                status=st.HTTP_401_UNAUTHORIZED,
            )
        elif pk:
            return run_and_respond(
                retrieve_records,
                self.model, self.serializer,
                start, num_of_records,
                pk=pk,
            )
        elif item_id:
            return run_and_respond(
                retrieve_records,
                self.model, self.serializer,
                start, num_of_records,
                item__id=item_id,
            )
        else:
            if not request.user.is_anonymous():
                return run_and_respond(
                    retrieve_records,
                    self.model, self.serializer,
                    start, num_of_records,
                    item__owner__id=request.user.id,
                )


class TransactionList(XListAPIView):

    model = ItemTransactionRecord
    # For serialization
    serializer = TransactionSerializer

    num_of_records = 8

    def get(self, request):
        start, num_of_records = self.paginator(request)
        user = request.user
        data, status = retrieve_records(
            ItemTransactionRecord, TransactionSerializer,
            start, num_of_records,
            giver=user,
        )
        data_2, status_2 = retrieve_records(
            ItemTransactionRecord, TransactionSerializer,
            start, num_of_records,
            receiver=user,
        )
        # Future: use better algorithm to merge and sort
        data = data + data_2
        if (status is st.HTTP_404_NOT_FOUND and
                status_2 is st.HTTP_404_NOT_FOUND):
            status = st.HTTP_404_NOT_FOUND
        else:
            status = st.HTTP_200_OK
        return Response(data=data, status=status)


class TransactionDetail(XDetailAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        perms.IsGiverOrReceiverOrNoPermission,
    )

    model = ItemTransactionRecord
    # For de-serialization
    deSerializer = TransactionSerializerLite
    # For serialization
    serializer = TransactionSerializer


class Timeline:
    def __init__(self, *models):
        """
        arguments <models> should take in several models, based on which
        one build a timeline array.
        """
        self.models = models    # the models you want to query to
        self.num_of_records = 10      # number of final records displayed
        # A common filter <dict> that will apply to all querysets
        # from all models.
        # For instance, self.common_filter = {"owner": request.user}
        # will do a final filter to select only Posts or Items that belong to
        # the owner
        self.common_filter = None
        self.starts = [0] * len(models)
        self.order_by = ["-time_updated"] * len(models)
        self.filter_type = ["and"] * len(models)
        # record the final count of records in each model that get into
        # the result; for instance,
        # when self.num_of_records = 10, one might have
        # 3 posts, 4 items and 3 item-edit-records.
        self.final_content_counts = [0] * len(models)

    def config(self, **kwargs):
        """
        configure <starts>, <order_by> and <num_of_records>, etc, properties.
        order_by and starts should be of type list, matching the <models>.
        """
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def ordering_field(self, queryset):
        import re
        if not queryset:
            return None
        instance = queryset[0]
        index = self.models.index(type(instance))
        # remove "-""
        minus = re.compile("^-")
        if minus.match(self.order_by[index]):
            ordering_field = self.order_by[index][1:]
        return ordering_field

    def merge(self, *querysets):
        num_of_arrays = len(querysets)
        result = []
        if num_of_arrays == 1:
            return querysets[0]
        if num_of_arrays == 2:
            a, b = querysets
            while a and b:
                if getattr(a[0], self.ordering_field(a)) > getattr(b[0], self.ordering_field(b)):
                    result.append(a.pop(0))
                else:
                    result.append(b.pop(0))
            if a:
                result = result + a
            else:
                result = result + b
            return result
        else:
            prev_results = [querysets[0]]
            for step in range(0, num_of_arrays - 1):
                sub_result = self.merge(
                    prev_results[step], querysets[step+1]
                )
                prev_results.append(sub_result)
            result = prev_results[num_of_arrays - 1]
        return result

    def get(self, *args, **kwargs):
        """
        Take in either an array of kwargs for filtering, e.g.
        get(
            {"item": item, "item__owner": request.user},
            {"item__owner": user}
        ), matching each of the <models>,
        or a common **kwargs to search,
        e.g. get(item=item, item__owner=request.user).
        Return:
            - list (mergesorted)
        """
        querysets = []
        from django.db.models import Q
        for index in range(0, len(self.models)):
            start = self.starts[index]
            model = self.models[index]
            print("\t index = %s, model = %s " % (index, model))
            if not kwargs:
                temp_kwargs = args[index]
                if self.filter_type[index] == "or":
                    Q_list = []
                    for field in temp_kwargs:
                        print("field = %s;" % (field))
                        value = temp_kwargs[field]
                        if type(value) is list:
                            for sub_value in value:
                                Q_list.append(Q(**{field: sub_value}))
                        else:
                            Q_list.append(Q(**{field: value}))
                    print(Q_list)
                    import operator
                    queryset = (model.objects
                                .filter(
                                    reduce(operator.or_, Q_list)
                                )
                                .order_by(self.order_by[index])
                                [start: start + self.num_of_records + 1])
                elif self.filter_type[index] == "and":
                    queryset = (model.objects.filter(**temp_kwargs)
                                .order_by(self.order_by[index])
                                [start: start + self.num_of_records + 1])
            else:
                queryset = (model.objects.filter(**kwargs)
                            .order_by(self.order_by[index])
                            [start: start + self.num_of_records + 1])
            if self.common_filter:
                queryset = queryset.filter(**self.common_filter)
            print("\n\tqueryset for model %s is %s" % (model, queryset))
            queryset = [r for r in queryset]
            querysets.append(queryset)
        # Merge sort
        print("\n\tquerysets = %s" % (querysets))
        timeline = self.merge(*querysets)[0:self.num_of_records]
        return timeline


class FeedList(XListAPIView):

    models = (Post, Item, ItemEditRecord, )
    serializer = (PostSerializer, ItemSerializer, ItemEditRecordSerializer, )
    order_by = ("-time_posted", "-time_created", "-time_updated", )
    filter_type = ["or", "or", "or"]

    def get(self, request):
        user = request.user
        params = request.query_params
        starts = [0] * len(self.models)
        if "starts" in params:
            starts = params['starts'].split(",")
        tl = Timeline(*self.models)
        tl.config(
            order_by=self.order_by,
            filter_type=self.filter_type,
            starts=starts,
        )
        interested_areas = user.interested_areas().split(",")
        query_args = [
            {"area": interested_areas},
            {"owner": user},
            {"item__owner": user},
        ]
        feeds = tl.get(*query_args)
        data = []
        for record in feeds:
            index = self.models.index(type(record))
            serializer = self.serializer[index]
            data.append(serializer(record).data)
        return Response(data=data)
