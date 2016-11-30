from django.conf.urls import patterns, url

from .views import IndexView,CreateView, DetailView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<config_id>[^/]+)/$', DetailView.as_view(), name='detail'),
    #url(r'^(?P<instance_name>[^/]+)/(?P<instance_id>[^/]+)/(?P<provider>[^/]+)/(?P<region>[^/]+)/create/$', 
    #    CreateView.as_view(),name='create'),
)
