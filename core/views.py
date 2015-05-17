__author__ = 'dongtao'
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
import datetime
from django.utils.timezone import get_current_timezone
from survey.models import Survey


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return render(request, 'homepage.html', {})


class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        import datetime
        import itertools

        total_responses = list(
            itertools.chain.from_iterable(map(
                lambda s: getattr(s, "responses").all(), self.request.user.surveys.all())))

        today_responses = []

        for response in total_responses:
            if response.created.date() > (datetime.datetime.now(tz=get_current_timezone()) - datetime.timedelta(days=1)).date():
                today_responses.append(response)

        all_surveys = Survey.objects.all().order_by('created').reverse()

        return {"num_total_responses": len(total_responses), "num_today_responses": len(today_responses),
                "surveys": reversed(self.request.user.surveys.all()), 'all_surveys': all_surveys}


