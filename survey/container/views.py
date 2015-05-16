__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render
from django.db.transaction import atomic
from django_ajax.decorators import ajax
from django.http.response import HttpResponseForbidden
from django_ajax.mixin import AJAXMixin
from guardian.mixins import PermissionRequiredMixin
from guardian.decorators import permission_required_or_403
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


class TextContainerUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = TextContainerForm
    template_name = 'survey/container/help-text.edit.html'
    model = TextContainer
    pk_url_kwarg = 'container_pk'
    permission_required = 'survey.change_textcontainer'
    raise_exception = True

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'survey/container/help-text.display.html', {'textcontainer': self.object})



@ajax
def move_container_up(request, container_pk=None):
    container = Container.objects.get(id=container_pk)
    if not container.has_change_permission(request.user):
        return HttpResponseForbidden()
    try:
        with atomic():
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
    container = Container.objects.get(id=container_pk)
    if not container.has_change_permission(request.user):
        return HttpResponseForbidden()
    try:
        with atomic():
            container_down = Container.objects.get(page=container.page, order=container.order + 1)
            container.order += 1
            container_down.order -= 1
            container_down.save()
            container.save()
        return True
    except:
        raise Exception("Cannot move down the last container")



class ContainerDeleteView(AJAXMixin, DeleteView):
    model = Container
    pk_url_kwarg = 'container_pk'

    # def get_success_url(self):
    #     return

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.has_delete_permission(request.user):
            return HttpResponseForbidden()

        with atomic():
            for p in Container.objects.filter(order__gt=self.object.order).filter(page=self.object.page):
                p.order -= 1
                p.save()
            self.object.delete()
            return True


