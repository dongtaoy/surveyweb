__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from .views import PageCreateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SurveyWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/$', PageCreateView.as_view(), name="page.create"),

)
