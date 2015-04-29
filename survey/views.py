__author__ = 'dongtao'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.db.transaction import atomic
from guardian.mixins import PermissionRequiredMixin
from survey.models import Survey, QuestionType, Page
from survey.forms import SurveyFrom



class SurveryDetailView(PermissionRequiredMixin, DetailView):
    model = Survey
    template_name = "survey/survey.detail.html"
    pk_url_kwarg = 'survey'
    context_object_name = 'survey'
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
            page = Page.objects.create(survey=survey)
            page.save()
        return redirect(reverse_lazy("survey.detail", kwargs={"survey": survey.id}))


class SurveyUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = SurveyFrom
    model = Survey
    pk_url_kwarg = 'survey'
    permission_required = 'survey.change_survey'
    template_name = 'survey/survey.builder.html'
    context_object_name = 'survey'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(SurveyUpdateView, self).get_context_data(**kwargs)
        context['questiontypes'] = QuestionType.objects.all()
        context['pages'] = self.object.pages.all()
        return context


class SurveyDeleteView(PermissionRequiredMixin, DeleteView):
    model = Survey
    pk_url_kwarg = 'survey'
    permission_required = 'survey.delete_survey'
    success_url = reverse_lazy("dashboard")


