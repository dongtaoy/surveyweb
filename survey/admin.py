__author__ = 'dongtao'
from django.contrib import admin
from survey.models import Survey, Category, QuestionType, Page

admin.site.register(Survey)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(QuestionType)