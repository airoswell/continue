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
    url(r'^user/$', views.user_profile, name='user-profile'),
    url(r'^user/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^user/collection/$', views.collection, name='collection'),
    url(r'^post/$',
        views.post_create, name='post_create'),
    url(r'^post/(?P<pk>[a-z0-9]+)/$',
        views.post, name='post'),
    url(r'^post/(?P<pk>[a-z0-9]+)/delete/$',
        views.post_delete, name='post_delete'),
    url(r'^item/$',
        views.item_create, name='item_create'),
    url(r'^item/(?P<pk>[a-z0-9]+)/timeline/$',
        views.item_timeline, name='item_timeline'),
    url(r'^item/(?P<pk>[a-z0-9]+)/delete/$',
        views.item_delete, name='item_delete'),
    url(r'^user/(?P<pk>[a-z0-9]+)/timeline/$',
        views.user_timeline, name='user_timeline'),
    url(r'^donations/$',
        views.donations, name='donations'),
    url(r'^activity-signup/$',
        views.activity, name='activity-signup'),
    url(r'^404/$', views.NotFound, name='404-not-found'),
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
    url(r'^posts/(?P<pk>[a-z0-9]+)/$',
        api.PostDetail.as_view(), name='post_detail'),
    url(r'^posts/(?P<post_id>[a-z0-9]+)/items/?$',
        api.ItemList.as_view(), name='post_items'),
    url(r'^items/?$', api.ItemList.as_view(), name='item_list'),
    url(r'^items/(?P<pk>[a-z0-9]+)/$',
        api.ItemDetail.as_view(),
        name='item_datail'),
    url(r'^bulk-items/$',
        api.BulkItemCreation.as_view(),
        name='bulk_item_creation'),
    url(r'^items/(?P<item_id>[a-z0-9]+)/updates/?$',
        api.ItemUpdateList.as_view(),
        name='item_updates'),
    url(r'^updates/$', api.ItemUpdateList.as_view(), name='update_list'),
    url(r'^profiles/$', api.UserDetails.as_view(), name='user_detail'),
    url(r'^profiles/(?P<pk>[a-z0-9]+)/$',
        api.UserDetails.as_view(), name='user_detail'),
    url(r'^user/messages/$',
        api.MessageList.as_view(),
        name='message_list'),
    url(r'^transactions/$',
        api.TransactionList.as_view(),
        name='transaction_list'),
    url(r'^transactions/(?P<pk>[a-z0-9]+)/$',
        api.TransactionDetail.as_view(),
        name='transaction_Detail'),
    url(r'^feeds/$',
        api.Feed.as_view(),
        name='feed_list'),
    url(r'^timeline/$',
        api.DashboardTimeline.as_view(),
        name='timeline_list'),
    url(r'^timeline/item/$',
        api.ItemTimeline.as_view(),
        name='item-timeline'),
    url(r'^timeline/user/$',
        api.UserTimeline.as_view(),
        name='user-timeline'),
    url(r'^images/$',
        api.ImageList.as_view(),
        name='image_list'),
    url(r'^images/(?P<pk>[a-z0-9]+)/$',
        api.ImageDetail.as_view(),
        name='image_detail'),
    url(r'^attendants/$',
        api.AttendentList.as_view(),
        name='attendant_list'),
)

# postman URL
urlpatterns += patterns(
    "postman",
    url(r'^user/inbox/(?:(?P<option>'+OPTIONS+')/)?$',
        InboxView.as_view(), name='inbox'),
    url(r'^user/reply/(?P<message_id>[[a-z0-9]]+)/$',
        ReplyView.as_view(), name='reply'),
    url(r'^user/view/(?P<message_id>[[a-z0-9]]+)/$',
        MessageView.as_view(), name='view'),
    url(r'^user/view/t/(?P<thread_id>[[a-z0-9]]+)/$',
        ConversationView.as_view(), name='view_conversation'),
)

urlpatterns += patterns(
    "",
    (r'^user/', include('allauth.urls')),
)
