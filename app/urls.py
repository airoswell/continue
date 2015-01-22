from django.conf.urls import patterns, url, include
# ======== Postman ========
from postman.views import InboxView, ReplyView, MessageView, ConversationView
from postman import OPTIONS
from app import views, api

urlpatterns = patterns(
    'page',
    # URL for pages
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^user/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^post/(?P<pk>\d+)/$',
        views.post_edit, name='post_edit'),
    url(r'^post/$',
        views.post_create, name='post_create'),
    url(r'^item/(?P<pk>\d+)/timeline/$',
        views.item_timeline, name='item_timeline'),
    url(r'^user/(?P<pk>\d+)/timeline/$',
        views.user_timeline, name='user_timeline'),
    url(r'^donations/$',
        views.donations, name='donations'),
)

# Django-allauth
urlpatterns += patterns(
    "",
    (r'^user/logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),
)
# ====================================================================
# =================== Django-Rest-Framework API ======================
urlpatterns += patterns(
    "api",
    url(r'^posts/?$', api.PostList.as_view(), name='post_list'),
    url(r'^posts/(?P<pk>\d*)/$',
        api.PostDetail.as_view(), name='post_detail'),
    url(r'^posts/(?P<post_id>\d*)/items/?$',
        api.ItemList.as_view(), name='post_items'),
    url(r'^items/?$', api.ItemList.as_view(), name='item_list'),
    url(r'^items/(?P<pk>[0-9]+)/$',
        api.ItemDetail.as_view(),
        name='item_datail'),
    url(r'^bulk-items/$',
        api.BulkItemCreation.as_view(),
        name='bulk_item_creation'),
    url(r'^items/(?P<item_id>[0-9]+)/histories/?$',
        api.HistoryList.as_view(),
        name='item_histories'),
    url(r'^histories/$', api.HistoryList.as_view(), name='history_list'),
    url(r'^profiles/$', api.UserDetails.as_view(), name='user_detail'),
    url(r'^profiles/(?P<pk>[0-9]+)/$',
        api.UserDetails.as_view(), name='user_detail'),
    url(r'^user/messages/$',
        api.MessageList.as_view(),
        name='message_list'),
    url(r'^transactions/$',
        api.TransactionList.as_view(),
        name='transaction_list'),
    url(r'^transactions/(?P<pk>[0-9]+)/$',
        api.TransactionDetail.as_view(),
        name='transaction_Detail'),
    url(r'^feeds/$',
        api.FeedList.as_view(),
        name='feed_list'),
    url(r'^timeline/$',
        api.TimelineList.as_view(),
        name='timeline_list'),
    url(r'^images/$',
        api.ImageList.as_view(),
        name='image_list'),
)

# postman URL
urlpatterns += patterns(
    "postman",
    url(r'^user/inbox/(?:(?P<option>'+OPTIONS+')/)?$',
        InboxView.as_view(), name='inbox'),
    url(r'^user/reply/(?P<message_id>[\d]+)/$',
        ReplyView.as_view(), name='reply'),
    url(r'^user/view/(?P<message_id>[\d]+)/$',
        MessageView.as_view(), name='view'),
    url(r'^user/view/t/(?P<thread_id>[\d]+)/$',
        ConversationView.as_view(), name='view_conversation'),
)

urlpatterns += patterns(
    "",
    (r'^user/', include('allauth.urls')),
)
