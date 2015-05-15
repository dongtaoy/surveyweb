__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import TextContainerCreateView, move_container_up

urlpatterns = (

    url(r"^create/text/$", login_required(TextContainerCreateView.as_view()),
        name="container.text.create"),

    url(r"^(?P<container_pk>\d+)/up/$", 'survey.container.views.move_container_up', name="container.move.up"),
)