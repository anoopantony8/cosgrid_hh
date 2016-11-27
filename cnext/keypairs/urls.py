from django.conf.urls import patterns, url
from .views import IndexView, CreateView, ImportView, DownloadView, AccountChange, GenerateView, DetailView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$',  CreateView.as_view(), name='create'),
    url(r'^(?P<keypairs_id>[^/]+)/$', DetailView.as_view(), name='detail'),
    url(r'account/account_change',AccountChange.as_view(),name = 'account'),
    
)
