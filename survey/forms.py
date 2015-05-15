__author__ = 'dongtao'
from django import forms
from survey.models import Survey, QuestionContainer, Choice, TextContainer
from django.forms.models import inlineformset_factory


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['creator', 'status']


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







