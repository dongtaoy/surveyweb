__author__ = 'dongtaoy'
from django.views.generic.edit import UpdateView
from guardian.mixins import PermissionRequiredMixin
from survey.forms import SurveyFrom
from survey.forms import Survey

class BuilderUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = SurveyFrom
    model = Survey
    pk_url_kwarg = 'survey'
    permission_required = 'survey.change_survey'
    template_name = 'survey/builder/survey.builder.html'



