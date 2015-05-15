__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import TextContainerCreateView, TextContainerUpdateView

urlpatterns = (

    url(r"^create/text/$", login_required(TextContainerCreateView.as_view()),
        name="container.text.create"),

    url(r"^(?P<container_pk>\d+)/edit/$", login_required(TextContainerUpdateView.as_view()),
        name="container.text.edit"),

    url(r"^(?P<container_pk>\d+)/up/$", 'survey.container.views.move_container_up', name="container.move.up"),

    url(r"^(?P<container_pk>\d+)/down/$", 'survey.container.views.move_container_down', name="container.move.down"),
)