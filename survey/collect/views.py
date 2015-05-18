__author__ = 'GC-Mac'

from guardian.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django_ajax.mixin import AJAXMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect
from survey.models import ResponseCollector, Survey
from survey.forms import CollectForm


class CollectCreateView(CreateView):
    model = ResponseCollector
    form_class = CollectForm
    template_name = "survey/collect/survey.collect.edit.html"

    def dispatch(self, request, *args, **kwargs):
        # print kwargs
        survey = Survey.objects.get(id=kwargs['survey'])
        if not request.user.has_perm('survey.change_survey', survey):
            raise PermissionDenied()
        return super(CollectCreateView, self).dispatch(request, args, kwargs)

    def form_valid(self, form):
        print self
        import uuid
        self.object = form.save(commit=False)
        self.object.survey = Survey.objects.get(id=self.kwargs['survey'])
        self.object.uuid = str(uuid.uuid4())
        self.object.save()
        return redirect(reverse_lazy('survey.collect', kwargs={'survey': self.object.survey.id}))


class CollectUpdateView(UpdateView):
    model = ResponseCollector
    form_class = CollectForm
    pk_url_kwarg = "collect"
    template_name = "survey/collect/survey.collect.edit.html"
    # success_url = reverse_lazy('survey.collect', kwargs={'survey': self.object.survey.id}))

    def get_success_url(self):
        return reverse_lazy('survey.collect', kwargs={'survey': self.object.survey.id})


class CollectDeleteView(AJAXMixin, DeleteView):
    model = ResponseCollector
    pk_url_kwarg = 'collect'

    def get_success_url(self):
        pass

    def delete(self, request, *args, **kwargs):
        super(CollectDeleteView, self).delete(request, args, kwargs)
        return True