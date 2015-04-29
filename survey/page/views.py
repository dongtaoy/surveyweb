__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponse
from django.db.transaction import atomic
from django.shortcuts import render
from survey.models import Page, Survey
from guardian.mixins import PermissionRequiredMixin
import json


class PageCreateView(CreateView):
    model = Page
    template_name = "survey/page/survey.builder.page.html"
    fields = ['survey']
    

    def form_valid(self, form):
        with atomic():
            page = form.save()
        return render(self.request, 'survey/page/survey.builder.page.html', {'page': page})
        # return HttpResponse(
        #     json.dump()
        #
        #     content_type="application/json"
        # )

#
# class PageDeleteView(DeleteView):
#
#     pass