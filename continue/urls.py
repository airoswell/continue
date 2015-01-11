from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns(
    '',
    url(r"^$", RedirectView.as_view(pattern_name="index")),
    url(r'^postman/',
        include('postman.urls')
        ),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
        ),
    (r'^search/', include('haystack.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('app.urls')),
)
