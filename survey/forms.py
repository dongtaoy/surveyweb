__author__ = 'dongtao'
from django.forms import ModelForm
from survey.models import Survey, QuestionContainer


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['creator', 'status']


class QuestionForm(ModelForm):
    pass