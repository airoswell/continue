# Models and serializers
from app.models import Item, Post, UserProfile
from app.models import ItemEditRecord, ItemTransactionRecord, PostItemStatus
from app.serializers import *
import app.permissions as perms
from app.errors import *
from GenericAPI import *
from app.CRUD import *
# Django Core
from django.shortcuts import redirect
# Django Rest Framework
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework import permissions
# ================================
# Django Allauth
from allauth.socialaccount.models import SocialToken
# Other Python module
from controllers import *


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
    items_per_page = 20

    def get(self, request, format=None):
        self.get_object()
        params = request.query_params
        page, items_per_page = self.paginator(request)
        # Display list of posts of a specified user
        if "user_id" in params:
            return run_and_respond(
                retrieve_records,
                Post, PostSerializerLite,
                page, items_per_page,
                owner__id=params["user_id"]
            )
        # Display list of posts of a location
        elif "zip_code" in params:
            return run_and_respond(
                retrieve_records,
                Post, PostSerializerLite,
                page, items_per_page,
                zip_code=params['zip_code']
            )
        # Display all posts of the current user
        return run_and_respond(
            retrieve_records,
            Post, PostSerializer,
            page, items_per_page,
            owner__id=request.user.id
        )

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
        if "items" in data:
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
        print("\tpost_error_handler.errors = %s" % (post_error_handler.errors))
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
            post = crud.update(data, owner=request.user)
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
    items_per_page = 20

    def get(self, request, post_id=None, format=None):
        page, items_per_page = self.paginator(request)
        # get list of items owned by a specific user
        # Don't need any authentication
        if request.GET.get("user_id"):
            return run_and_respond(
                retrieve_records,
                Item, ItemSerializer,
                page, items_per_page,
                owner__id=request.GET.get("user_id"),
                visibility="Public",
            )
        # For accessing items of a post
        # No authentication required
        elif post_id:
            return run_and_respond(
                retrieve_records,
                Item, ItemSerializer,
                page, items_per_page,
                status_in_post__post__id=post_id,
            )
        # get list of items of the current authenticated user
        elif not request.user.is_anonymous():
            return run_and_respond(
                retrieve_records,
                Item, ItemSerializer,
                page, items_per_page,
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
        perms.IsOwnerOrNoPermission,
    )

    def get(self, request):
        user = request.user
        if user.is_anonymous():
            return Response(data=[], status=st.HTTP_401_UNAUTHORIZED)
        if user.socialaccount_set.all():
            provider = user.socialaccount_set.all()[0]
            provider_name = provider.get_provider().name
            social_account_uid = provider.uid
            social_account_photo = provider.get_avatar_url()
            access_token = SocialToken.objects.filter(
                account__user=user,
                account__provider=provider.provider
            )[0].token
        else:
            provider_name = ""
            social_account_uid = ""
            social_account_photo = ""
            access_token = ""
        # In case multiple user profiles were created,
        # choose the latest one
        from django.core.exceptions import MultipleObjectsReturned
        try:
            profile = UserProfile.objects.get(user__id=user.id)
        except AssertionError:
            profile = (UserProfile.objects.filter(user__id=user.id)
                                  .order_by('time_created')[0])
        except MultipleObjectsReturned:
            profile = (UserProfile.objects.filter(user__id=user.id)
                                  .order_by('time_created')[0])
        user_info = {
            "name": profile.name,
            "id": user.id or None,
            "is_anonymous": user.is_anonymous(),
            "zip_code": profile.zip_code,
            "email": profile.email,
            "social_account_provider": provider_name or "",
            "social_account_uid": social_account_uid or "",
            "social_account_photo": social_account_photo or "",
            "social_account_access_token": access_token,
        }
        return Response(
            data=[user_info], status=st.HTTP_200_OK
        )


from haystack.query import SearchQuerySet


class S:
    def __init__(self, model):
        self.model = model

    def search(self, params):
        zip_code = ""
        if "zip_code" in params:
            zip_code = params['zip_code']
        # Note that the default ordering of models are not respected here
        if params["q"] != "":
            sqs = (SearchQuerySet().models(Post).filter(content=params['q'])
                   .order_by("-time_posted"))
        else:
            sqs = SearchQuerySet().models(Post).all().order_by("-time_posted")
        if zip_code != "":
            sqs = sqs.filter(zip_code=zip_code)
        results = [sq.object for sq in sqs]
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
    items_per_page = 20

    permission_classes = (perms.IsOwnerOrNoPermission,)

    def get(self, request, pk=None, item_id=None):
        page, items_per_page = self.paginator(request)
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
                page, items_per_page,
                pk=pk,
            )
        elif item_id:
            return run_and_respond(
                retrieve_records,
                self.model, self.serializer,
                page, items_per_page,
                item__id=item_id,
            )
        else:
            if not request.user.is_anonymous():
                return run_and_respond(
                    retrieve_records,
                    self.model, self.serializer,
                    page, items_per_page,
                    item__owner__id=request.user.id,
                )


class TransactionList(XListAPIView):

    model = ItemTransactionRecord
    # For serialization
    serializer = TransactionSerializer

    items_per_page = 8

    def get(self, request):
        page, items_per_page = self.paginator(request)
        user = request.user
        data, status = retrieve_records(
            ItemTransactionRecord, TransactionSerializer,
            page, items_per_page,
            giver=user,
        )
        data_2, status_2 = retrieve_records(
            ItemTransactionRecord, TransactionSerializer,
            page, items_per_page,
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
