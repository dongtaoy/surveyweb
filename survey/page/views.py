__author__ = 'dongtaoy'
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render
from django.db.transaction import atomic
from guardian.mixins import PermissionRequiredMixin
from django_ajax.mixin import AJAXMixin
from survey.models import Page, Survey


class PageCreateView(CreateView):
    model = Page
    fields = ['survey']

    def form_valid(self, form):
        page = form.save()
        return render(self.request, 'survey/page/survey.page.html', {'page': page})


class PageDeleteView(AJAXMixin, PermissionRequiredMixin, DeleteView):
    model = Page
    permission_required = 'survey.delete_page'
    raise_exception = True
    pk_url_kwarg = 'page'

    def get_success_url(self):
        pass

    def delete(self, *args, **kwargs):
        try:
            with atomic():
                self.object = self.get_object()
                for p in Page.objects.filter(order__gt=self.object.order).filter(survey=self.object.survey):
                    p.order -= 1
                    p.save()
                self.object.delete()
                return True
        except:
            return False


class PageUpdateView(AJAXMixin, PermissionRequiredMixin, UpdateView):
    model = Page
    permission_required = 'survey.change_page'
    raise_exception = True
    pk_url_kwarg = 'page'
    fields = ['order']

    def form_valid(self, form):
        self.object = self.get_object()
        if form.cleaned_data['order'] == 0:
            return False
        else:
            try:
                with atomic():
                    page = Page.objects.get(survey=self.object.survey, order=form.cleaned_data['order'])
                    page.order = self.object.order
                    page.save()
                    form.save()
                    return True
            except:
                return False






