__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render
from survey.models import QuestionContainer, QuestionType
from survey.forms import QuestionForm, ChoiceFormSet


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    success_url = '/'
    question_type = None

    def dispatch(self, request, *args, **kwargs):
        if request.GET:
            self.question_type = QuestionType.objects.get(id=request.GET['questionType'])
        return super(QuestionCreateView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return QuestionType.objects.get(id=self.request.GET['questionType']).get_edit_template_name()

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        if self.request.GET:
            if self.question_type.get_name() != 'single-textbox':
                context['formset'] = ChoiceFormSet(instance=QuestionContainer())
        return context

    def form_valid(self, form):
        question = form.save(commit=False)
        if question.questiontype.get_name() != 'single-textbox':
            choiceformset = ChoiceFormSet(self.request.POST, instance=question)
            if choiceformset.is_valid():
                question.save()
                texts = set()
                for form in choiceformset:
                    if 'text' in form.cleaned_data.keys():
                        if form.cleaned_data['text'] not in texts:
                            choice = form.save(commit=False)
                            choice.question = question
                            choice.save()
                            texts.add(form.cleaned_data['text'])
        else:
            question.save()
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


class QuestionUpdateView(UpdateView):
    form_class = QuestionForm
    model = QuestionContainer
    pk_url_kwarg = 'question'

    def get_template_names(self):
        return self.object.questiontype.get_edit_template_name()

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)

        if self.object.questiontype.get_name() != 'single-textbox':
            context['formset'] = ChoiceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        question = form.save(commit=False)
        if question.questiontype.get_name() != 'single-textbox':
            choiceformset = ChoiceFormSet(self.request.POST, instance=question)
            if choiceformset.is_valid():
                question.save()
                choiceformset.save()
            else:
                question.save()
                texts = set()
                for form in choiceformset:
                    if 'text' in form.cleaned_data.keys():
                        if form.cleaned_data['text'] not in texts:
                            choice = form.save(commit=False)
                            choice.question = question
                            choice.save()
                            texts.add(form.cleaned_data['text'])
        else:
            question.save()
        return render(self.request, question.questiontype.get_display_template_name(), {'question': question})


