__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import TextContainerCreateView

urlpatterns = (

    url(r"^create/text/$", login_required(TextContainerCreateView.as_view()),
        name="container.text.create"),

)