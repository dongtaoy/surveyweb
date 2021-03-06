__author__ = 'dongtao'
from formtools.wizard.views import SessionWizardView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http.response import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.db.transaction import atomic
from guardian.mixins import PermissionRequiredMixin
from survey.models import Survey, QuestionType, Page, ResponseCollector, Category, Response
from survey.forms import SurveyForm, ResponseForm

#list all surveys
class SurveyListView(ListView):
    model = Survey
    template_name = "survey/survey.list.html"
    context_object_name = "surveys"
    # allow_empty = False
    # def get_queryset(self):
    # return Survey.objects.filter()

    def get_queryset(self):
        try:
            category = Category.objects.get(id=self.request.GET['category'])
            object_list = self.model.objects.filter(category=category)
            return object_list
        except:
            return self.model.objects.all()


    def get_context_data(self, **kwargs):
        context = super(SurveyListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        try:
            context['current'] = Category.objects.get(id=self.request.GET['category'])
        except:
            pass
        return context


#view detail of a survey
class SurveyDetailView(PermissionRequiredMixin, DetailView):
    model = Survey
    template_name = "survey/survey.detail.html"
    pk_url_kwarg = 'survey'
    context_object_name = 'survey'
    permission_required = 'survey.view_survey'
    raise_exception = True


#create a survey
class SurveyCreateView(CreateView):
    template_name = "survey/survey.create.html"
    success_url = reverse_lazy("view.detail")
    form_class = SurveyForm

    def form_valid(self, form):
        with atomic():
            survey = form.save(commit=False)
            survey.creator = self.request.user
            survey.save()
            page = Page.objects.create(survey=survey)
            page.save()
        return redirect(reverse_lazy("survey.detail", kwargs={"survey": survey.id}))


#enter survey builder to edit a survey
class SurveyUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = SurveyForm
    model = Survey
    pk_url_kwarg = 'survey'
    permission_required = 'survey.change_survey'
    template_name = 'survey/survey.builder.html'
    context_object_name = 'survey'
    raise_exception = True
    # success_url = reverse_lazy('survey.builder', kwargs={'survey': })

    def get_context_data(self, **kwargs):
        context = super(SurveyUpdateView, self).get_context_data(**kwargs)
        context['questiontypes'] = QuestionType.objects.all()
        context['pages'] = self.object.pages.all()
        return context

    def get_success_url(self):
        return reverse_lazy('survey.builder', kwargs={'survey': self.object.id})

        # def form_valid(self, form):
        # self.object = form.save()
        #     return HttpResponse(1)


#delete a survey
class SurveyDeleteView(PermissionRequiredMixin, DeleteView):
    model = Survey
    pk_url_kwarg = 'survey'
    permission_required = 'survey.delete_survey'
    success_url = reverse_lazy("dashboard")


#enter collector for a specific survey
class SurveyCollectView(PermissionRequiredMixin, DetailView):
    model = Survey
    template_name = "survey/survey.collect.html"
    pk_url_kwarg = 'survey'
    context_object_name = 'survey'
    permission_required = 'survey.view_survey'
    raise_exception = True

    def get_object(self, queryset=None):
        import uuid
        object = super(SurveyCollectView, self).get_object(queryset)
        if object.status != Survey.OPEN:
            object.status = Survey.OPEN
            object.save()
        if len(object.collectors.all()) == 0:
            ResponseCollector.objects.create(survey=object,
                                             status=ResponseCollector.OPEN,
                                             name="Web collector 1",
                                             uuid=str(uuid.uuid4()))
        return object


#preview a survey
class SurveyPreviewView(SessionWizardView):
    template_name = 'survey/survey.do.html'

    def done(self, form_list, **kwargs):
        return redirect(reverse_lazy('survey.builder', kwargs={'survey': self.kwargs['survey']}))

    def get_context_data(self, form, **kwargs):
        context = super(SurveyPreviewView, self).get_context_data(form, **kwargs)
        context['survey'] = Survey.objects.get(id=self.kwargs['survey'])
        return context

    def get_form_kwargs(self, step=None):
        return {
            'page': Page.objects.get(order=int(step) + 1, survey=self.kwargs['survey'])
        }


#enter analysis page of a survey
class SurveyAnalyzeView(PermissionRequiredMixin, DetailView):
    model = Survey
    template_name = "survey/survey.analyze.html"
    pk_url_kwarg = "survey"
    context_object_name = 'survey'
    permission_required = 'survey.view_survey'
    raise_exception = True


#enter a page to do a survey
class SurveyDoView(SessionWizardView):
    template_name = 'survey/survey.do.html'

    def done(self, form_list, **kwargs):
        from django.contrib.auth.models import User
        collector = ResponseCollector.objects.get(uuid=self.kwargs['collectuuid'])
        if not self.request.user.is_authenticated():
            user = User.objects.get(id=-1)
        else:
            user = self.request.user
        response = Response.objects.create(survey=collector.survey, interviewee=user, collector=collector)
        for form in form_list:
            form.save(user=self.request.user, response=response)
        return redirect(reverse_lazy('home'))

    def get_context_data(self, form, **kwargs):
        context = super(SurveyDoView, self).get_context_data(form, **kwargs)
        context['survey'] = Survey.objects.get(id=self.kwargs['survey'])
        return context

    def get_form_kwargs(self, step=None):

        return {
            'page': Page.objects.get(order=int(step) + 1, survey=self.kwargs['survey'])
        }

#render all forms in a survey
def preview_survey_factory(request, *args, **kwargs):
    survey = Survey.objects.get(id=kwargs['survey'])
    if not (request.user.has_perm('survey.view_survey', survey)):
        raise PermissionDenied()

    ret_form_list = [ResponseForm for i in survey.pages.all()]

    class ReturnClass(SurveyPreviewView):
        form_list = ret_form_list

    return ReturnClass.as_view()(request, *args, **kwargs)


#render all forms in a survey for others to do
def do_survey_factory(request, *args, **kwargs):
    collect = ResponseCollector.objects.get(uuid=kwargs['collectuuid'])
    if collect.status == ResponseCollector.CLOSED:
        raise PermissionDenied()
    kwargs['survey'] = collect.survey.id
    ret_form_list = [ResponseForm for i in collect.survey.pages.all()]

    # return HttpResponseForbidden()
    class ReturnClass(SurveyDoView):
        form_list = ret_form_list

    return ReturnClass.as_view()(request, *args, **kwargs)




