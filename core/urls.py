from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from core.views import DashboardView

urlpatterns = patterns(
    '',
    # Examples:

    url(r'^$', 'core.views.home', name='home'),

    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),

    url(r'^403$', login_required(TemplateView.as_view(template_name='common/403.html'))),
    url(r'^collector', TemplateView.as_view(template_name='page/collector.html')),

    # common page testing
    # url(r'^403$', login_required(TemplateView.as_view(template_name='common/403.html'))),
    url(r'^404$', login_required(TemplateView.as_view(template_name='common/404.html'))),
    url(r'^500$', login_required(TemplateView.as_view(template_name='common/500.html'))),
    url(r'^delconfirm/$', login_required(TemplateView.as_view(template_name='common/delete.confirmation.html')), name='delete.confirmation'),
)

