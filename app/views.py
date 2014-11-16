from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import RegUser, Item, Post, PassEvent, ItemPostRelation
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
import pdb
from controllers import *

# Create your views here.


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
        # pdb.set_trace()
        return HttpResponse(json.dumps(
            {
                'incoming': post_data,
                'success': success,
                'msg': msg,
                'new_post': post[0],
            }
        ))
    # Edit existed post
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


def results_view(request):
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
            'search_loc': search_loc,
            'search_string': search_string,
        }
    )


def results_process(request):
    search_string = request.GET.get("search_string")
    search_loc = request.GET.get("search_loc")
    # If user only specified both the location and item name,
    # search the intersecting results;
    # otherwise, search all posts in the location.
    if len(search_string) > 3:
        posts_queryset = Post.objects.filter(
            zip_code=search_loc,
            item__title__icontains=search_string
        )
    else:
        posts_queryset = Post.objects.filter(
            zip_code=search_loc,
        )
    posts = posts_writer(posts_queryset)
    response = {
        'string': search_string,
        'loc': search_loc,
    }
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
    pdb.set_trace()
    data = json.loads(request.body)
    try:
        new_user = RegUser.objects.create_user(
            username=data['user_name'],
            email=data['email'],
            password=data['password']
        )
    except IntegrityError:
        pdb.set_trace()
        return HttpResponse(json.dumps(
            {
                'success': False,
                "msg": "Username is already taken!",
            }
        ))
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
