__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import QuestionCreateView

urlpatterns = (

    url(r"^create/$", login_required(QuestionCreateView.as_view()),
        name="question.create"),

)