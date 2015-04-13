__author__ = 'dongtao'
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return render(request, 'homepage.html', {})


class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        import datetime, itertools
        total_responses = list(
            itertools.chain.from_iterable(map(
                lambda s: getattr(s, "responses").all(), self.request.user.surveys.all())))

        today_responses = filter(lambda res: res.created == datetime.datetime.today(), total_responses)

        return {"num_total_responses": len(total_responses), "num_today_responses": len(today_responses),
                 "surveys": reversed(self.request.user.surveys.all())}


