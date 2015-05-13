__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render
from survey.models import TextContainer
from survey.forms import TextContainerForm


class TextContainerCreateView(CreateView):
    form_class = TextContainerForm
    template_name = 'survey/container/helptext-edit.html'

    def form_valid(self, form):
        container = form.save()
        print container
        return HttpResponse(1)

    def get_initial(self):
        if self.request.GET:
            return {
                'page': self.request.GET['page'],
                'type': self.request.GET['containerType']
            }

