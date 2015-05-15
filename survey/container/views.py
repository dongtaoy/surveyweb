__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render
from django.db.transaction import atomic
from django_ajax.decorators import ajax
from survey.forms import TextContainerForm
from survey.models import TextContainer, Container


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


class TextContainerUpdateView(UpdateView):
    form_class = TextContainerForm
    template_name = 'survey/container/help-text.edit.html'
    model = TextContainer
    pk_url_kwarg = 'container_pk'

    def form_valid(self, form):
        print form
        self.object = form.save()
        print self.object.text
        return render(self.request, 'survey/container/help-text.display.html', {'textcontainer': self.object})



@ajax
def move_container_up(request, container_pk=None):
    try:
        with atomic():
            container = Container.objects.get(id=container_pk)
            container_up = Container.objects.get(page=container.page, order=container.order - 1)
            container.order -= 1
            container_up.order += 1
            container_up.save()
            container.save()
        return True
    except:
        raise Exception("Cannot move up the first container")


@ajax
def move_container_down(request, container_pk=None):
    try:
        with atomic():
            container = Container.objects.get(id=container_pk)
            container_down = Container.objects.get(page=container.page, order=container.order + 1)
            container.order += 1
            container_down.order -= 1
            container_down.save()
            container.save()
        return True
    except:
        raise Exception("Cannot move down the last container")



