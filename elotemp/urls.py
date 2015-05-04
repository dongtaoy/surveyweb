__author__ = 'zhangjingyuan'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from elotemp.views import EloView,EloResult


urlpatterns = patterns(
    '',
    #url(r'^create/$',login_required(EloCreate.as_view()),name='elo.create'),
    url(r'^demo/$', 'elotemp.views.init_elo', name='elo.init_views'),
    url(r'^demo/result/$',login_required(EloResult.as_view()),name='elo.result'),
    url(r'^demo/(?P<step>\d+)/$', login_required(EloView.as_view()), name='elo.views'),
    url(r'^demo/(?P<step>\d+)/(?P<result>\d)/$', 'elotemp.views.update_rank', name='elo.update'),
)