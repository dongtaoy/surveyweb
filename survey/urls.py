from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from survey.views import SurveyCreateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SurveyWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url("^create/$", login_required(SurveyCreateView.as_view()), name="survey_create"),


)
