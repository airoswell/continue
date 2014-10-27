from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns(
    '',
    # general URL that any one can access
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
    url(
        r'^results/process/$',
        views.results_process,
        name='results_process'
    ),
    url(r'^post/(?P<post_id>\d*)/$', views.post, name='post'),
    url(r'^get_user/$', views.get_user, name='get_user'),
    url(r'^login/$', views.login_view, name='user_login'),
    url(
        r'^signup/$',
        views.signup,
        name='user_signup',
    ),
    # Only logged in user can access
    url(r'^user/$', views.user_view, name='user'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^user/compose/$', views.compose, name='compose'),
    url(
        r'^user/compose/process/$',
        views.compose_process,
        name='compose_process'
    ),
)
