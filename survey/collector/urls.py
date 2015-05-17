__author__ = 'GC-Mac'

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import CollectorCreateView, CollectorUpdateView, CollectorDeleteView


urlpatterns = patterns('',
    url(r'^create/$', login_required(CollectorCreateView.as_view()), name="collector.create"),
    url(r'^(?P<collector>\d+)/edit/$', login_required(CollectorUpdateView.as_view()), name='collector.edit'),
    url(r'^(?P<collector>\d+)/delete/$', login_required(CollectorDeleteView.as_view()), name='collector.delete'),
    )
