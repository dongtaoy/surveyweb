__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import QuestionContainerCreateView

urlpatterns = (

    url(r"^create/type/(?P<questiontype>\d+)/$", login_required(QuestionContainerCreateView.as_view()),
        name="question.create"),

)