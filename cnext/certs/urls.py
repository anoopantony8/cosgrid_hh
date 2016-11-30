from django.conf.urls import patterns, url

from .views import IndexView, DetailView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<cert_id>[^/]+)/$', DetailView.as_view(), name='detail'),
   )
