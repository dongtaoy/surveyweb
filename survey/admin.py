__author__ = 'dongtao'
from django.contrib import admin
from survey.models import Survey, Category

admin.site.register(Survey)
admin.site.register(Category)