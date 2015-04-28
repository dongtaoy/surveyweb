from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from survey.views import SurveyCreateView, SurveryDetailView, SurveyDeleteView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SurveyWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url("(?P<survey>\d+)/$", login_required(SurveryDetailView.as_view()), name="survey.detail"),

    url("^create/$", login_required(SurveyCreateView.as_view()), name="survey.create"),

    url("^delete/(?P<survey>\d+)$", login_required(SurveyDeleteView.as_view()), name="survey.delete"),

)
