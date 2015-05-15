__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render
from survey.forms import TextContainerForm


class TextContainerCreateView(CreateView):
    form_class = TextContainerForm
    template_name = 'survey/container/help-text.edit.html'


    def form_valid(self, form):
        container = form.save()
        return render(self.request, 'survey/container/help-text.display.html', {'textcontainer': container})

    def get_initial(self):
        if self.request.GET:
            return {
                'page': self.request.GET['page'],
                'type': self.request.GET['containerType']
            }

