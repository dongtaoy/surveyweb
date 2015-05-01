__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from survey.models import QuestionContainer, QuestionType


class QuestionContainerCreateView(CreateView):
    model = QuestionContainer
    fields = ['page', 'question', 'questiontype']
    # template_name = ''

    def get_template_names(self):
        return QuestionType.objects.get(id=self.kwargs['questiontype']).get_edit_template_name()