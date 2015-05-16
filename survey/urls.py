__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from survey.views import SurveyCreateView, SurveryDetailView, SurveyDeleteView, SurveyUpdateView, SurveyCollectView, \
    SurveyPreviewView, SurveyAnalyzeView
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'SurveyWeb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r"^(?P<survey>\d+)/$", login_required(SurveryDetailView.as_view()), name="survey.detail"),

                       url(r"^create/$", login_required(SurveyCreateView.as_view()), name="survey.create"),

                       url(r"^(?P<survey>\d+)/delete/$", login_required(SurveyDeleteView.as_view()),
                           name="survey.delete"),

                       url(r"^(?P<survey>\d+)/edit/$", login_required(SurveyUpdateView.as_view()),
                           name="survey.builder"),

                       url(r"^(?P<survey>\d+)/collect/$", login_required(SurveyCollectView.as_view()),
                           name="survey.collect"),

                       url(r"^(?P<survey>\d+)/preview/$", 'survey.views.preview_survey_factory', name='survey.preview'),

                       url(r"^(?P<survey>\d+)/do/$", 'survey.views.do_survey_factory', name='survey.do'),

                       url(r"^(?P<survey>\d+)/analyze/$",
                           login_required(SurveyAnalyzeView.as_view()), name='survey.analyze'),

                       url(r"^page/", include('survey.page.urls')),

                       url(r"^question/", include('survey.question.urls')),

                       url(r"^container/", include('survey.container.urls')),
                       )
