from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import RegUser, Item, Post, PassEvent, ItemStatus
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
# Create your views here.


class ItemOverview:
    def __init__(self, item_id, title, quantity, condition, detail):
        self.item_id = item_id
        self.title = title
        self.quantity = quantity
        self.condition = condition
        self.detail = detail


class PostOverview:
    def __init__(self, post_id, title, zip_code, owner, detail):
        self.post_id = post_id
        self.title = title
        self.zip_code = zip_code
        self.owner = owner
        self.items = []
        self.detail = detail

    def addItem(self, item):
        self.items.append(item)


def get_posts(posts_queryset):
    """
    A global function: turn a queryset of post to
    simple JSON serializable objects
    """
    posts = []
    for post in posts_queryset:
        post_overview = PostOverview(
            post_id=post.id,
            title=post.title,
            zip_code=post.zip_code,
            owner=post.owner.username,
            detail=post.detail
        )
        for item in post.item.all():
            new_item = ItemOverview(
                item_id=item.id,
                title=item.title,
                quantity=item.quantity,
                condition=item.condition,
                detail=item.detail
            )
            post_overview.addItem(new_item.__dict__)
        posts.append(post_overview.__dict__)
    return posts


def index(request):
    return render(
        request,
        'app/index.html',
        {
            'view': 'index',
            'user_id': request.user.id,
            'is_anonymous': request.user.is_anonymous(),
        }
    )


def compose(request):
    return render(
        request,
        'app/compose.html',
        {
            'view': 'compose',
        }
    )


def compose_process(request):
    if request.method == 'POST':
        current_user = RegUser.objects.get(username=request.user.username)
        data = json.loads(request.body)
        post = data['post']
        response = {
            'msg': 'I received your new post!!',
            'posted_by': current_user.username,
            'received_title': post['title']
        }
        new_post = Post(
            title=post['title'],
            owner=current_user,
            zip_code=post['zip_code'],
            detail=post['detail'],
        )
        new_post.save()
        # Build all Item and ItemStatus objects
        for item in data['items']:
            current_item = Item(
                title=item['title'],
                quantity=item['quantity'],
                condition=item['condition'],
                detail=item['detail'],
            )
            current_item.save()
            item_status = ItemStatus(
                item=current_item,
                post=new_post,
                item_status='av',
            )
            item_status.save()
        return HttpResponse(json.dumps(response))


def results(request):
    # Initialize date passed from search input
    if request.GET:
        data = request.GET
        search_loc = data['search-loc']
        search_string = data['search-string']
    else:
        search_loc = ""
        search_string = ""

    return render(
        request,
        'app/results.html',
        {
            'view': 'results',
            'listvar': 'this is results view',
            'search_loc': search_loc,
            'search_string': search_string,
        }
    )


def results_process(request):
    search_string = request.GET.get("search_string")
    search_loc = request.GET.get("search_loc")

    if len(search_string) > 0:
        posts_queryset = Post.objects.filter(
            zip_code=search_loc,
            item__title__icontains=search_string
        )
    elif len(search_string) == 0:
        posts_queryset = Post.objects.filter(
            zip_code=search_loc,
        )
    posts = get_posts(posts_queryset)
    return HttpResponse(json.dumps(posts))


def get_user(request):
    """
    return basic infomation about the current user; requested by 'layout.html'
    to set global $scope.user_info variable.
    """
    response = {
        "user_info": {
            'is_anonymous': request.user.is_anonymous(),
            'user_id': request.user.id,
            'username': request.user.username,
        }
    }
    return HttpResponse(json.dumps(response))


def user_view(request):
    """
    A view function that respond to URL '/app/user/', which display
    the admin page of the current user.

    If the current user is not logged in, redirect to '/app/login/'
    page
    """
    if request.method == 'POST':
        posts_queryset = Post.objects.filter(owner__id=request.user.id).all()
        posts = get_posts(posts_queryset)
        return HttpResponse(json.dumps(posts))
    elif request.user.is_anonymous():
        return HttpResponseRedirect("/app/login/")
    return render(
        request,
        'app/user.html',
        {
            'view': 'user',
        }
    )


def user_info_generator(user):
    """
    Take in a User object, return a simple objects containing
    basic information about the User.
    """
    user_info = {
        'user_name': '',
        'user_id': '',
        'is_anonymous': True,
    }
    if user.is_anonymous() is False:
        user_info['user_name'] = user.username
        user_info['user_id'] = user.id
        user_info["is_anonymous"] = False
    return user_info


def login_handler(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            user_info = user_info_generator(user)
            request_status = "Logged in"
        else:
            request_status = "Disabled"
    else:
        request_status = "Invalid"
    response = {
        'user_info': user_info,
        'request_status': request_status,
    }
    return user, response


def login_view(request):
    # If the user has not logged in
    if request.method == 'POST':
        data = json.loads(request.body)
        user_name_input = data['user_name']
        password_input = data['password']
        user, response = login_handler(request, user_name_input, password_input)
        return HttpResponse(json.dumps(response))
    is_anonymous = True
    if request.user.is_anonymous():
        is_anonymous = True
    else:
        is_anonymous = False
    return render(
        request,
        'app/login.html',
        {
            'view': 'login',
            'is_anonymous': is_anonymous,
            'username': request.user.username,
        }
    )


def signup(request):
    data = json.loads(request.body)
    new_user = RegUser.objects.create_user(
        username=data['user_name'],
        email=data['email'],
        password=data['password']
    )
    if True:
        # If signup is successful
        user, response = login_handler(
            request,
            data['user_name'],
            data['password']
        )
        response['signup_is_success'] = True
    else:
        response['signup_is_success'] = False
    return HttpResponse(json.dumps(response))


def user_logout(request):
    logout(request)
    response = {
        'a': 'b'
    }
    return render(
        request,
        'app/logout.html',
        response,
    )


def post(request, post_id):
    post_queryset = Post.objects.filter(id=post_id)
    response = {
        'var_post': "variable from post()",
        'post_id': post_id,
    }
    return HttpResponse(json.dumps(response))
