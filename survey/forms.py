__author__ = 'dongtao'
from django import forms
from survey.models import Survey, QuestionContainer, Choice
from django.forms.models import inlineformset_factory


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['creator', 'status']


ChoiceFormSet = inlineformset_factory(QuestionContainer,
                                      Choice,
                                      fields=('text', ),
                                      can_delete=False,
                                      labels= {
                                          'text': 'choice'
                                      }, extra=1)


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








