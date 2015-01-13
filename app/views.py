# Models and serializers
from app.models import Item, Post
from app.models import ItemEditRecord, PostItemStatus, ItemTransactionRecord
from app.api import S
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
    return render(
        request,
        'pages/search.html',
        {
            'view': 'search',
            "posts": posts,
            "user": user_info_generator(request.user)
        }
    )


def post_edit(request, pk):
    queryset = Post.objects.filter(pk=pk)
    if not queryset:
        return Response(
            data={"error": "item with pk value %s Not found" % (pk)},
            status=st.HTTP_404_NOT_FOUND
        )
    post = queryset[0]
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


class Timeline:
    def __init__(self, *models):
        """
        arguments <models> should take in several models, based on which
        one build a timeline array.
        """
        self.models = models
        self.starts = [0] * len(models)
        self.order_by = ["-time_updated"] * len(models)
        self.interval = 8
        self.filter_type = ["and"] * len(models)
        self.common_filter = None

    def config(self, **kwargs):
        """
        configure <starts>, <order_by> and <interval> properties.
        order_by and starts should be of type list, matching the <models>.
        """
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def field(self, index):
        import re
        minus = re.compile("^-")
        if minus.match(self.order_by[index]):
            field = self.order_by[index][1:]
        return field

    def merge(self, *args):
        num_of_arrays = len(args)
        result = []
        if num_of_arrays == 1:
            return args[0]
        if num_of_arrays == 2:
            a = args[0]
            b = args[1]
            while a and b:
                if getattr(a[0], self.field(0)) > getattr(b[0], self.field(1)):
                    result.append(a.pop(0))
                else:
                    result.append(b.pop(0))
            if a:
                result = result + a
            else:
                result = result + b
            return result
        else:
            for step in range(0, num_of_arrays - 1):
                result = self.merge(args[step], args[step + 1])
        return result

    def get(self, *args, **kwargs):
        """
        Take in either an array of kwargs for filtering, e.g.
        get(
            {"item": item, item__owner: request.user},
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
            if not kwargs:
                temp_kwargs = args[index]
                if self.filter_type[index] == "or":
                    Q_list = []
                    for kwarg in temp_kwargs:
                        Q_list.append(Q(**{kwarg: temp_kwargs[kwarg]}))
                    import operator
                    queryset = model.objects.filter(
                        reduce(operator.or_, Q_list)
                    )
                elif self.filter_type[index] == "and":
                    queryset = (model.objects.filter(**temp_kwargs)
                                .order_by(self.order_by[index])
                                [start: start + self.interval + 1])
            else:
                queryset = (model.objects.filter(**kwargs)
                            .order_by(self.order_by[index])
                            [start: start + self.interval + 1])
            if self.common_filter:
                queryset = queryset.filter(**self.common_filter)
            queryset = [r for r in queryset]
            querysets.append(queryset)
        # Merge sort
        timeline = self.merge(*querysets)
        print(timeline)
        return timeline


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
    if "items_per_page" in params:
        items_per_page = params['items_per_page']
    else:
        items_per_page = 8

    queryset = Item.objects.filter(pk=pk)
    if not queryset:
        return Response(
            data={"error": "item with pk value %s Not found" % (pk)},
            status=st.HTTP_404_NOT_FOUND
        )
    item = queryset[0]

    tl = Timeline(ItemEditRecord, ItemTransactionRecord)
    tl.config(
        interval=items_per_page,
        starts=(edit_start, transaction_start)
    )
    timeline = tl.get(item=item)[0: tl.interval]
    return render(
        request,
        'pages/item-timeline.html',
        {
            'view': 'timeline',
            'timeline': timeline,
            "item": item,
        }
    )


def user_timeline(request, pk):
    tl = Timeline(ItemEditRecord, ItemTransactionRecord)
    tl.config(
        interval=16,
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
    posts = Post.objects.filter(owner=user)
    interested_areas = user.profile.all()[0].interested_areas
    areas = interested_areas.split(",")
    num = len(areas)
    models = [Post] * num
    print("\tareas = %s" %(areas))
    print("\tmodels = %s" %(models))
    tl = Timeline(*models)
    query_args = []
    for area in areas:
        print(area)
        query_args.append({"area": area})
    print(query_args)
    tl.config(
        interval=8, order_by=["-time_posted"] * num,
    )
    feeds = tl.get(*query_args)
    # load pending transactions
    tl = Timeline(ItemTransactionRecord)
    tl.config(
        interval=16, filter_type=["or"],
        common_filter={"status": "Sent"}
    )
    transactions = tl.get({"receiver": user, "giver": user})
    for transaction in transactions:
        if transaction.status != "Sent":
            transactions.remove(transaction)
    # Build a combined timeline of ItemEditRecord and ItemTransactionRecord
    tl = Timeline(ItemEditRecord, ItemTransactionRecord)
    tl.config(interval=16, filter_type=["and", "or"])
    timeline = tl.get(
        {"item__owner": user},
        {"giver": user, "receiver": user},
    )[0: tl.interval]
    return render(
        request,
        'pages/dashboard.html',
        {
            'view': 'dashboard',
            'feeds': feeds,
            'posts': posts,
            'timeline': timeline,
            'transactions': transactions,
        }
    )
