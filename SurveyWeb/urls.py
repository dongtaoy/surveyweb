from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'SurveyWeb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^accounts/', include('allauth.urls')),

                       url(r'^djangojs/', include('djangojs.urls')),


                       url(r'^', include("core.urls")),

                       url(r'^survey/', include("survey.urls")),


                       url(r'^aboutus/', TemplateView.as_view(template_name='page/aboutus.html'), name="aboutus"),
                       url(r'^elo/', login_required(TemplateView.as_view(template_name='page/elo.html'))),
                       url(r'^editor/', login_required(TemplateView.as_view(template_name='builder/builder.html')),
                           name="builder"),
                       url(r'^summary/', login_required(TemplateView.as_view(template_name='page/summary.html')),
                           name="summary")
                       )
