__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render
from survey.models import QuestionContainer, QuestionType
from survey.forms import QuestionForm


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    success_url = '/'

    def get_template_names(self):
        return QuestionType.objects.get(id=self.request.GET['questionType']).get_edit_template_name()

    # def get_context_data(self, **kwargs):
    #     context = super(QuestionCreateView, self).get_context_data(**kwargs)
    #     context['type'] = self.kwargs['questiontype']
    #     return context

    def form_valid(self, form):
        question = form.save(commit=True)
        return render(self.request, question.questiontype.get_display_template_name(), {'question': question})

    def get_initial(self):
        if self.request.GET:
            return {
                'questiontype': self.request.GET['questionType'],
                'page': self.request.GET['page'],
                'type': self.request.GET['containerType']
            }
        else:
            return super(QuestionCreateView, self).get_initial()


