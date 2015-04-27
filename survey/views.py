__author__ = 'dongtao'
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.db.transaction import atomic
from core.models import Survey
from core.forms import SurveyFrom


class SurveryDetailView(DetailView):
    model = Survey
    template_name = "survey/survey.detail.html"
    pk_url_kwarg = 'survey'


class SurveyCreateView(CreateView):
    template_name = "survey/survey.create.html"
    success_url = reverse_lazy("dashboard")
    form_class = SurveyFrom

    def form_valid(self, form):
        with atomic():
            survey = form.save(commit=False)
            survey.creator = self.request.user
            survey.save()
        return redirect(reverse_lazy("survey.detail", kwargs={"survey": survey.id}))


