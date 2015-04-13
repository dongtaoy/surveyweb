__author__ = 'dongtao'
from django.forms import ModelForm
from core.models import Survey


class SurveyFrom(ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['creator']
