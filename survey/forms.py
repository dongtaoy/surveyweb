__author__ = 'dongtao'
from django import forms
from survey.models import Survey, QuestionContainer, Choice, TextContainer, Response, Container, QuestionType, \
    AnswerText, AnswerBase, AnswerCheck, AnswerRadio, AnswerSelect
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['creator', 'status']

class IgnoreSameValueInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(IgnoreSameValueInlineFormSet, self).clean()
        print 'in'
        values = set()
        for form in self.forms:
            if 'text' in form.cleaned_data.keys():
                print form.cleaned_data['text']
                # if form.cleaned_data['text'] in values:
                #     del form
                values.add(form.cleaned_data['text'])

        # for form in self.forms:
        #     if 'text' in form.cleaned_data.keys():
        #         print form.cleaned_data['text']
        #         if form.cleaned_data['text'] not in values:
        #             del form

ChoiceFormSet = inlineformset_factory(QuestionContainer,
                                      Choice,
                                      fields=('text', ),
                                      can_delete=True,
                                      labels={
                                          'text': 'choice'
                                      },
                                      min_num=1,
                                      validate_min=True,
                                      extra=1, )




class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionContainer
        exclude = ['order']

        labels = {
            'question': 'Please enter your question here...'
        }

        widgets = {
            'questiontype': forms.HiddenInput,
            'page': forms.HiddenInput,
            'type': forms.HiddenInput
        }


class TextContainerForm(forms.ModelForm):
    class Meta:
        model = TextContainer
        exclude = ['order']

        labels = {
            'text': 'Please enter your text here...'
        }

        widgets = {
            'page': forms.HiddenInput,
            'type': forms.HiddenInput
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        exclude = ['survey', 'interviewee']

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        super(ResponseForm, self).__init__(*args, **kwargs)

        for container in self.page.containers.all():
            if container.type == Container.QUESTION:
                question = container.questioncontainer
                if question.questiontype == QuestionType.objects.get(name='Single Textbox'):
                    self.fields["question_%d" % question.pk] = forms.CharField(label=question.question,
                                                                               widget=forms.Textarea(
                                                                                   attrs={'placeholder': ''}),
                                                                               required=question.required)
                elif question.questiontype == QuestionType.objects.get(name='Multiple Choice'):
                    question_choices = question.get_choices()

                    self.fields["question_%d" % question.pk] = forms.ChoiceField(label=question.question,
                                                                                 widget=forms.RadioSelect,
                                                                                 choices=question_choices,
                                                                                 required=question.required)
                elif question.questiontype == QuestionType.objects.get(name='Dropdown'):
                    question_choices = question.get_choices()
                    # question_choices = tuple([('', '---------')]) + question_choices
                    self.fields["question_%d" % question.pk] = forms.ChoiceField(label=question.question,
                                                                                 choices=question_choices,
                                                                                 required=question.required)
                elif question.questiontype == QuestionType.objects.get(name='Checkbox'):
                    question_choices = question.get_choices()
                    self.fields["question_%d" % question.pk] = forms.MultipleChoiceField(label=question.question,
                                                                                         widget=forms.CheckboxSelectMultiple,
                                                                                         choices=question_choices,
                                                                                         required=question.required)
            if container.type == Container.TEXT:
                textcontainer = container.textcontainer
                self.fields["help_%d" % textcontainer.pk] = forms.CharField(label=textcontainer.text,
                                                                            widget=forms.HiddenInput, required=False)



    def save(self, commit=True, **kwargs):
        user = kwargs.pop('user')
        response = super(ResponseForm, self).save(commit=False)
        response.survey = self.page.survey
        response.interviewee = user
        response.save()

        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith("question_"):
                question_id = int(field_name.split("_")[1])
                print field_name, field_value

                # Choice.objects.get(text=field_value)
                question = QuestionContainer.objects.get(pk=question_id)
                if question.questiontype == QuestionType.objects.get(name='Single Textbox'):
                    answer = AnswerText(question=question)
                    answer.text = field_value
                elif question.questiontype == QuestionType.objects.get(name='Multiple Choice'):
                    answer = AnswerRadio(question=question)
                    answer.choice = Choice.objects.get(question=question, text=field_value)
                elif question.questiontype == QuestionType.objects.get(name='Dropdown'):
                    answer = AnswerSelect(question=question)
                    answer.choice = Choice.objects.get(question=question, text=field_value)
                elif question.questiontype == QuestionType.objects.get(name='Checkbox'):
                    answer = AnswerCheck(question=question)
                    answer.choice = Choice.objects.get(question=question, text=field_value)
                answer.response = response
                answer.save()

        return response



