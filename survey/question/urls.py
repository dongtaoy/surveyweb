__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import QuestionCreateView, QuestionUpdateView

urlpatterns = (

    url(r"^create/$", login_required(QuestionCreateView.as_view()),
        name="question.create"),

    url(r"^(?P<question>\d+)/edit/", login_required(QuestionUpdateView.as_view()), name="question.edit"),

    url(r"^(?P<question_pk>\d+)/data/", 'survey.question.views.question_data', name='question.data')
)