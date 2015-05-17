__author__ = 'GC-Mac'

from guardian.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from survey.models import ResponseCollector
from survey.forms import CollectorForm


class CollectorCreateView(CreateView):
    model = ResponseCollector
    form_class = CollectorForm
    template_name = "survey/collector/survey.collector.edit.html"


class CollectorUpdateView(UpdateView):
    model = ResponseCollector
    form_class = CollectorForm
    pk_url_kwarg = "collector"
    template_name = "survey/collector/survey.collector.edit.html"


class CollectorDeleteView(DeleteView):
    pass