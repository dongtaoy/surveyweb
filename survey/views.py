__author__ = 'dongtao'
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.db.transaction import atomic
from guardian.mixins import PermissionRequiredMixin
from survey.models import Survey
from survey.forms import SurveyFrom


class SurveryDetailView(PermissionRequiredMixin, DetailView):
    model = Survey
    template_name = "survey/survey.detail.html"
    pk_url_kwarg = 'survey'
    permission_required = 'survey.view_survey'
    raise_exception = True


class SurveyCreateView(CreateView):
    template_name = "survey/survey.create.html"
    success_url = reverse_lazy("view.detail")
    form_class = SurveyFrom

    def form_valid(self, form):
        with atomic():
            survey = form.save(commit=False)
            survey.creator = self.request.user
            survey.save()
        return redirect(reverse_lazy("survey.detail", kwargs={"survey": survey.id}))


class SurveyDeleteView(PermissionRequiredMixin, DeleteView):
    model = Survey
    pk_url_kwarg = 'survey'
    permission_required = 'survey.delete_survey'

    pass


