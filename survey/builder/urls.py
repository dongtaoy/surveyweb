__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import BuilderUpdateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SurveyWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'(?P<survey>\d+)$', BuilderUpdateView.as_view(), name="survey.builder"),
)
