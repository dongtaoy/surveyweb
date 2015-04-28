__author__ = 'dongtao'
from django.contrib import admin
from survey.models import Survey, Category, QuestionType

admin.site.register(Survey)
admin.site.register(Category)
admin.site.register(QuestionType)