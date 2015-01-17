# Models and serializers
from app.models import Item, Post
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

# =======Should be removed in production========
# ================================
# Other Python module
import json
from controllers import *


# Handel all user-related posts request
def user_posts(request):
    data = json.loads(request.body)
    user = request.user
    # return all posts by the user
    if data['type'] == 'get':
        posts = user_get_posts(user)
        return HttpResponse(json.dumps(posts))
    # Create new post
    elif data['type'] == 'create':
        post_data = data['post']
        success, msg, post = user_create_post(post_data, request.user)
        post = posts_writer([post])
        return HttpResponse(json.dumps(
            {
                'incoming': post_data,
                'success': success,
                'msg': msg,
                'new_post': post[0],
            }
        ))
    # Edit existing post
    elif data['type'] == 'edit':
        post_data = data['post']
        success, msg, post = user_edit_post(post_data, request.user)
        post = posts_writer([post])
        return HttpResponse(json.dumps(
            {
                'success': success,
                'msg': msg,
                'post': post[0],
            }
        ))
    elif data['type'] == 'delete':
        post_data = data['post']
        success, msg = user_delete_post(post_data, request.user)
        if success:
            return HttpResponse(json.dumps(
                {
                    'success': success,
                }
            ))


def user_info_generator(user):
    """
    Take in a User object, return a simple objects containing
    basic information about the User.
    """
    user_info = {
        'name': '',
        'id': '',
        'is_anonymous': True,
        'social_account_provider': ""
    }
    if not user.is_anonymous():
        user_info['name'] = user.username
        user_info['id'] = user.id
        user_info["is_anonymous"] = False
        if user.socialaccount_set.all():
            provider = user.socialaccount_set.all()[0]
            user_info['social_account_provider'] = provider.get_provider().name
            user_info['social_account_photo'] = provider.get_avatar_url()
    return user_info


# All pages
def index(request):
    return render(
        request,
        # 'app/index.html',
        'index.html',
        {
            'view': 'index',
            "user": user_info_generator(request.user)
        }
    )


def search(request):
    # Initialize date passed from search input
    params = request.GET
    s = S(Post)
    posts = s.search(params)
    area = ""
    q = ""
    if "area" in params:
        area = params["area"]
    if "q" in params:
        q = params['q']
    return render(
        request,
        'pages/search.html',
        {
            'view': 'search',
            "posts": posts,
            "user": user_info_generator(request.user),
            "q": q,
            "area": area,
            "init_post_num": len(posts),
        }
    )


def post_edit(request, pk):
    user = request.user
    if user.is_anonymous():
        return redirect("index")
    queryset = Post.objects.filter(pk=pk)
    if not queryset:
        return Response(
            data={"error": "item with pk value %s Not found" % (pk)},
            status=st.HTTP_404_NOT_FOUND
        )
    post = queryset[0]
    if user != post.owner:
        return redirect("index")
    items = post.items.all()
    return render(
        request,
        'pages/post.html',
        {
            'view': 'post',
            'post': post,
            "items": items,
        }
    )


def post_create(request):
    if request.user.is_anonymous():
        return redirect("index")
    return render(
        request,
        'pages/post.html',
        {
            'view': 'post',
        }
    )


def item_timeline(request, pk):
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

    queryset = Item.objects.filter(pk=pk)
    if not queryset:
        return Response(
            data={"error": "item with pk value %s Not found" % (pk)},
            status=st.HTTP_404_NOT_FOUND
        )
    item = queryset[0]

    tl = TimelineManager(ItemEditRecord, ItemTransactionRecord)
    tl.config(
        num_of_records=num_of_records,
        starts=(edit_start, transaction_start)
    )
    timeline = tl.get(item=item)[0: tl.num_of_records]
    if request.user == item.owner:
        subject = "You"
    else:
        subject = request.user.name()
    return render(
        request,
        'pages/item-timeline.html',
        {
            'view': 'timeline',
            'timeline': timeline,
            "item": item,
            'subject': subject
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


def dashboard(request):
    """
    A view function that respond to URL '/app/user/', which display
    the admin page of the current user.

    If the current user is not logged in, redirect to '/app/login/'
    page
    """
    user = request.user
    if user.is_anonymous():
        return redirect('/app/user/login/')
    params = request.GET
    numOfPosts = 10
    if "numOfPosts" in params:
        numOfPosts = params["numOfPosts"]
    posts = Post.objects.filter(owner=user)[:numOfPosts]
    # Build feeds (posts are from interested area)
    # need to include more stuffs in the future
    interested_areas = user.profile.all()[0].interested_areas
    tl = TimelineManager(Post, Item, ItemEditRecord, )
    tl.config(
        order_by=("-time_posted", "-time_created", "-time_updated", ),
        filter_type = ["or", "or", "or"],
        num_of_records=10,
    )
    interested_areas = user.interested_areas().split(",")
    query_args = [
        {"area": interested_areas},
        {"owner": user},
        {"item__owner": user},
    ]
    feeds = tl.get(*query_args)
    # Basically record counts from each model
    # specify starting points of next Ajax requests.
    feed_starts = {model.__name__: 0 for model in tl.models}
    for record in feeds:
        feed_starts[type(record).__name__] += 1
    # Build a combined timeline of ItemEditRecord and ItemTransactionRecord
    # of the current user.
    import pdb; pdb.set_trace()
    tl = TimelineManager(ItemEditRecord, ItemTransactionRecord)
    tl.config(num_of_records=16, filter_type=["and", "or"])
    timeline = tl.get(
        {"item__owner": user},
        {"giver": user, "receiver": user},
    )[0: tl.num_of_records]
    timeline_starts = {model.__name__: 0 for model in tl.models}
    for record in timeline:
        timeline_starts[type(record).__name__] += 1
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
        }
    )
