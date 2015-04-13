__author__ = 'dongtao'
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.db.transaction import atomic

from core.forms import SurveyFrom


class SurveyCreateView(CreateView):
    template_name = "survey/survey.create.html"
    success_url = reverse_lazy("dashboard")
    form_class = SurveyFrom

    def form_valid(self, form):
        with atomic():
            survey = form.save(commit=False)
            survey.creator = self.request.user
            survey.save()
        return redirect(self.success_url)