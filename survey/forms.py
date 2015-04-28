__author__ = 'dongtao'
from django.forms import ModelForm
from survey.models import Survey, Page


class SurveyFrom(ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['creator', 'status']

# class PageForm(ModelForm):
#     class Meta:
#         model = Page
#         exclude = ['created', 'updated', 'survey', 'order', 'title']