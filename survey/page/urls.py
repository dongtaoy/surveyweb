__author__ = 'dongtaoy'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import PageCreateView, PageDeleteView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SurveyWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/$', login_required(PageCreateView.as_view()), name="page.create"),

    url(r'^(?P<page>\d+)/delete/$', login_required(PageDeleteView.as_view()), name="page.delete")
)
