__author__ = 'dongtao'
from django.contrib import admin
from survey.models import Survey, Category, QuestionType, Page, QuestionContainer, Choice, AnswerBase, AnswerText, Response, AnswerChoice

admin.site.register(Survey)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(QuestionType)
admin.site.register(QuestionContainer)
admin.site.register(Choice)
admin.site.register(AnswerBase)
admin.site.register(AnswerText)
admin.site.register(Response)
admin.site.register(AnswerChoice)