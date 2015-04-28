from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from survey.views import SurveyCreateView, SurveryDetailView, SurveyDeleteView, SurveyUpdateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SurveyWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"(?P<survey>\d+)/$", login_required(SurveryDetailView.as_view()), name="survey.detail"),

    url(r"^create/$", login_required(SurveyCreateView.as_view()), name="survey.create"),

    url(r"^delete/(?P<survey>\d+)$", login_required(SurveyDeleteView.as_view()), name="survey.delete"),

    url(r"^build/(?P<survey>\d+)$", login_required(SurveyUpdateView.as_view()), name="survey.builder"),
    # url(r"builder/", include('survey.builder.urls'))
)
