# Models and serializers
from app.models import Item, Post
from app.models import CustomizedCharField, CustomizedNumField
from app.models import ItemEditRecord, PostItemStatus, ItemTransactionRecord
from app.api import S, TimelineManager
from app.GenericAPI import *
from app.serializers import *
from app.CRUD import *
from app.errors import *

#
# Django Core
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_control
# =======Should be removed in production========
# ================================
# Other Python module
import json
from django.db.models import Q
import operator


# All pages

def NotFound(request):
    return render(
        request,
        '404-not-found.html',
        {"target": 'page'},
    )


def index(request):
    return render(
        request,
        # 'app/index.html',
        'index.html',
        {
            'view': 'index',
        }
    )


def search(request):
    # Initialize date passed from search input
    params = request.GET
    content = ""
    areas = ""
    tags = ""
    secret_key = ""
    if "q" in params:
        content = params['q']
    if "areas" in params:
        areas = params["areas"]
    if "tags" in params:
        tags = params["tags"]
    if "secret_key" in params:
        secret_key = params['secret_key']
    s = S(Post)
    s.config(
        num_of_records=8,
    )
    if not secret_key:
        posts = s.__search__(
            content=content,
            areas=areas,
            tags=tags,
            visibility="Public",
        )
    else:
        posts = s.__search__(
            content=content,
            areas=areas,
            tags=tags,
            visibility="Invitation",
            secret_key=secret_key,
        )
    posts = [post.object for post in posts]
    return render(
        request,
        'pages/search.html',
        {
            'view': 'search',
            "posts": posts,
            "q": content,
            "areas": areas,
            "tags": tags,
            "secret_key": secret_key,
            "init_post_num": len(posts),
        }
    )


def post(request, pk):
    queryset = Post.objects.filter(pk=pk)
    if not queryset:
        return redirect("404-not-found")
    post = queryset[0]
    if post.visibility != "Public" and post.owner != request.user:
        return render(
            request,
            'unauthorized.html',
            {
                'view': 'post'
            }
        )
    items = post.items.all()
    return render(
        request,
        'pages/post.html',
        {
            'view': 'post',
            'post': post,
            "items": items,
            'LIVEHOST': settings.LIVEHOST,
            'is_owner': request.user == post.owner
        }
    )


@cache_control(no_cache=True, must_revalidate=True)
def post_create(request):
    if request.user.is_anonymous():
        return redirect("index")
    return render(
        request,
        'pages/post.html',
        {
            'view': 'post_create',
            'LIVEHOST': settings.LIVEHOST,
        }
    )


@cache_control(no_cache=True, must_revalidate=True)
def item_create(request):
    if request.user.is_anonymous():
        return redirect("index")
    return render(
        request,
        'pages/item.html',
        {
            'view': 'item',
            'LIVEHOST': settings.LIVEHOST,
        }
    )


@cache_control(no_cache=True, must_revalidate=True)
def post_delete(request, pk):
    if request.user.is_anonymous():
        return redirect("index")
    qs = Post.objects.filter(pk=pk)
    if not qs:
        return render(
            request,
            '404-not-found.html',
            {
                'target': "post",
                'LIVEHOST': settings.LIVEHOST,
            }
        )
    post = qs[0]
    post.delete()
    return render(
        request,
        'pages/delete.html',
        {
            'view': 'delete',
            'success': True,
            'message': "The post is successfully deleted.",
            'LIVEHOST': settings.LIVEHOST,
        }
    )


def item_delete(request, pk):
    if request.user.is_anonymous():
        return redirect("index")
    qs = Item.objects.filter(pk=pk)
    if not qs:
        return render(
            request,
            '404-not-found.html',
            {
                'target': "item",
                'LIVEHOST': settings.LIVEHOST,
            }
        )
    item = qs[0]
    ItemEditRecord.objects.filter(item=item).delete()
    CustomizedCharField.objects.filter(item=item).delete()
    CustomizedNumField.objects.filter(item=item).delete()
    item.delete()
    return render(
        request,
        'pages/delete.html',
        {
            'view': 'delete',
            "target": "item",
            'message': "The item is successfully deleted.",
            'LIVEHOST': settings.LIVEHOST,
        }
    )


def item_timeline(request, pk):
    queryset = Item.objects.filter(pk=pk)
    if not queryset:
        return render(
            request,
            '404-not-found.html',
            {
                'target': 'item',
                'LIVEHOST': settings.LIVEHOST,
            }
        )
    item = queryset[0]
    user = request.user
    authorized = ((user == item.owner) or
                  (user in item.previous_owners.all() and
                   item.visibility == 'Ex_owner') or
                  item.visibility == 'Public')
    if not authorized:
        return render(
            request,
            'unauthorized.html',
            {
                'view': 'timeline'
            }
        )
    params = request.GET
    if 'edit_start' in params:
        edit_start = params['edit_start']
    else:
        edit_start = 0
    if 'transaction_start' in params:
        transaction_start = params['transaction_start']
    else:
        transaction_start = 0
    if "num_of_records" in params:
        num_of_records = params['num_of_records']
    else:
        num_of_records = 8
    tl = TimelineManager(ItemEditRecord, ItemTransactionRecord)
    tl.config(
        num_of_records=num_of_records,
        starts=(edit_start, transaction_start)
    )
    timeline = tl.get(item=item)[0: tl.num_of_records]
    print("\t\nitem_timeline returned %s result in timeline" % (len(timeline)))
    # Prepare the init_starts
    init_starts = {model.__name__: 0 for model in tl.models}
    for record in timeline:
        init_starts[type(record).__name__] += 1
    return render(
        request,
        'pages/item-timeline.html',
        {
            'view': 'item-timeline',
            'timeline': timeline,
            "item": item,
            "init_starts": init_starts,
        }
    )


def user_timeline(request, pk):
    tl = TimelineManager(ItemEditRecord, ItemTransactionRecord)
    tl.config(
        num_of_records=16,
    )
    timeline = tl.get(item__owner=request.user)
    timeline.reverse()
    return render(
        request,
        'pages/user-timeline.html',
        {
            'view': 'timeline',
            'timeline': timeline,
        }
    )


def user_profile(request):
    """
    A view function that respond to URL '/app/user/?user_id', which display
    the user profile page of the specified user
    """
    user = request.user
    params = request.GET
    if not ("user_id" in params):
        return redirect('/app/')

    if not user.is_anonymous():
        if user.uid() == params["user_id"]:
            return redirect("dashboard")
    qs = User.objects.filter(profile__id=params['user_id'])
    if not qs:
        return render(
            request,
            "404-not-found.html",
            {"view": 'user-profile', "target": "page", }
        )
    target_user = qs[0]

    # Load posts
    numOfPosts = 10
    if "numOfPosts" in params:
        numOfPosts = params["numOfPosts"]
    posts = (Post.objects
             .filter(owner=target_user, visibility="Public")[:numOfPosts])

    # Build a combined timeline of ItemEditRecord and ItemTransactionRecord
    # of the current user.
    tl = TimelineManager(ItemEditRecord, ItemTransactionRecord)
    num_of_records = 10     # overwrite number of initial return here
    tl.config(num_of_records=num_of_records)

    if user.is_anonymous():
        Q_perm = Q(item__visibility="Public")
    else:
        Q_perm = reduce(operator.or_, (
            Q(item__visibility="Public"), reduce(operator.and_, (
                Q(item__visibility="Ex-owners"),
                Q(item__previous_owners__profile__id=user.uid())
            ))
        ))

    update_args = reduce(operator.and_, [
        Q(item__owner=target_user), Q_perm
    ])
    transfer_args = reduce(operator.and_, [
        reduce(operator.or_, [
            Q(giver=target_user),
            Q(receiver=target_user)
        ]),
        Q_perm,
    ])
    timeline = tl.get(
        update_args,
        transfer_args,
    )
    timeline_starts = {model.__name__: 0 for model in tl.models}
    for record in timeline:
        timeline_starts[type(record).__name__] += 1
    return render(
        request,
        'pages/user-profile.html',
        {
            'view': 'user-profile',
            'posts': posts,
            'numOfPosts': numOfPosts,
            'timeline': timeline,
            'timeline_starts': timeline_starts,
            'LIVEHOST': settings.LIVEHOST,
            "target_user": target_user,
        }
    )


@cache_control(no_cache=True, must_revalidate=True)
def dashboard(request):
    """
    A view function that respond to URL '/app/user/dashboard/', which display
    the admin page of the current user.

    If the current user is not logged in, redirect to '/app/login/'
    page
    """
    user = request.user
    params = request.GET
    if user.is_anonymous() and not ("user_id" in params):
        return redirect('/app/user/login/')
    post_kwargs = {"owner": user}
    # Load posts
    numOfPosts = 10
    if "numOfPosts" in params:
        numOfPosts = params["numOfPosts"]
    posts = Post.objects.filter(**post_kwargs)[:numOfPosts]

    # Feeds
    # Build feeds (posts are from interested area)
    # need to include more stuffs in the future
    interested_areas = user.profile.interested_areas
    tl = TimelineManager(Post, Item, ItemEditRecord, )
    tl.config(
        order_by=("-time_created", "-time_created", "-time_updated", ),
        filter_type = ["and", "or", "or"],
        num_of_records=10,
    )
    interested_areas = user.interested_areas().split(",")
    Ex_owners_Q = Q(
        visibility='Ex-owners', previous_owners=request.user
    )
    public_Q = Q(visibility='Public')
    areas_Q = Q(area__in=interested_areas)
    owner_Q = Q(owner=user)
    item_arg = reduce(
        operator.or_,
        [owner_Q, reduce(
            operator.and_,
            [areas_Q, reduce(
                operator.or_,
                [public_Q, Ex_owners_Q]
            )]
        )]
    )
    update_Ex_owners_Q = Q(
        item__visibility='Ex-owners',
        item__previous_owners=request.user
    )
    update_public_Q = Q(item__visibility='Public')
    update_areas_Q = Q(item__area__in=interested_areas)
    update_owner_Q = Q(item__owner=user)
    update_arg = reduce(
        operator.or_,
        [update_owner_Q, reduce(
            operator.and_,
            [update_areas_Q, reduce(
                operator.or_,
                [update_public_Q, update_Ex_owners_Q]
            )]
        )]
    )
    query_args = [
        {"area": interested_areas, "visibility": "Public"},
        item_arg,
        update_arg,
    ]
    feeds = tl.get(*query_args)
    # Basically record counts from each model
    # specify starting points of next Ajax requests.
    feed_starts = {model.__name__: 0 for model in tl.models}
    for record in feeds:
        feed_starts[type(record).__name__] += 1
    # Build a combined timeline of ItemEditRecord and ItemTransactionRecord
    # of the current user.
    tl = TimelineManager(ItemEditRecord, ItemTransactionRecord)
    tl.config(num_of_records=16, filter_type=["and", "or"])
    timeline = tl.get(
        {"item__owner": user},
        {"giver": user, "receiver": user},
    )[0: tl.num_of_records]
    timeline_starts = {model.__name__: 0 for model in tl.models}
    for record in timeline:
        timeline_starts[type(record).__name__] += 1

    available_tags = []
    items = Item.objects.filter(owner=user)
    for item in items:
        if item.tags:
            tags = item.tags.split(",")
            for tag in tags:
                if not (tag in available_tags):
                    available_tags.append(tag)
    return render(
        request,
        'pages/dashboard.html',
        {
            'view': 'dashboard',
            'feeds': feeds,
            'feed_starts': feed_starts,
            'posts': posts,
            'numOfPosts': numOfPosts,
            'timeline': timeline,
            'timeline_starts': timeline_starts,
            "subject": "You",
            'LIVEHOST': settings.LIVEHOST,
        }
    )


@cache_control(no_cache=True, must_revalidate=True)
def collection(request):
    """
    collection page
    """
    user = request.user
    params = request.GET
    if user.is_anonymous() and not ("user_id" in params):
        return redirect('/app/user/login/')

    available_tags = []
    items = Item.objects.filter(owner=user)
    for item in items:
        if item.tags:
            tags = item.tags.split(",")
            for tag in tags:
                if not (tag in available_tags):
                    available_tags.append(tag)

    available_tags = sorted(available_tags)
    return render(
        request,
        'pages/collection.html',
        {
            'view': 'collection',
            'LIVEHOST': settings.LIVEHOST,
            'available_tags': available_tags,
        }
    )


def donations(request):
    if "collector_uid" in request.GET:
        collector_uid = request.GET["collector_uid"]
        qs = User.objects.filter(profile__id=collector_uid)
        if not qs:
            return redirect("index")
    elif "collector_name" in request.GET:
        collector_name = request.GET["collector_name"]
        qs = User.objects.filter(profile__name=collector_name)
    if not qs:
        return redirect("index")
    collector_uid = qs[0].uid()
    return render(
        request,
        'pages/donations.html',
        {
            'view': "donations",
            'collector_uid': collector_uid,
        }
    )
