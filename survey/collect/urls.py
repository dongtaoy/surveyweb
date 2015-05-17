__author__ = 'GC-Mac'

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import CollectCreateView, CollectUpdateView, CollectDeleteView


urlpatterns = patterns('',
    url(r'^create/$', login_required(CollectCreateView.as_view()), name="collect.create"),
    url(r'^(?P<collect>\d+)/edit/$', login_required(CollectUpdateView.as_view()), name='collect.edit'),
    url(r'^(?P<collect>\d+)/delete/$', login_required(CollectDeleteView.as_view()), name='collect.delete'),
    )
