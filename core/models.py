__author__ = 'dongtao'
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)


class Survey(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    creator = models.ForeignKey(User, null=False, blank=False, related_name="surveys")
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    STATUS_CHOICES = (
        (OPEN, 'open'),
        
    )

    def get_questions(self):
        import itertools
        return list(itertools.chain.from_iterable(map(lambda p: getattr(p, 'containers').all(), self.pages.all())))





class Page(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    survey = models.ForeignKey(Survey, null=False, blank=False, related_name='pages')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ContainerType(models.Model):
    text = models.CharField(max_length=50, null=False, blank=False)


class Container(models.Model):
    page = models.ForeignKey(Page, null=False, blank=False, related_name="containers")
    sortid = models.IntegerField(null=False, blank=False)
    type = models.ForeignKey(ContainerType, null=True,  on_delete=models.SET_NULL)


class ImageSubContainer(models.Model):
    image = models.ImageField(null=False, blank=False)
    container = models.ForeignKey(Container, null=False, blank=False)


class TextSubContainer(models.Model):
    text = models.TextField(null=False, blank=False)
    container = models.ForeignKey(Container, null=False, blank=False)



class Image(models.Model):
    url = models.ImageField(null=False, blank=False)


class QuestionType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    helper = models.TextField(null=True, blank=True)


class Question(models.Model):
    name = models.TextField(null=False, blank=False)
    container = models.ForeignKey(Container, null=False, blank=False)
    type = models.ForeignKey(QuestionType)


class Choice(models.Model):
    text = models.TextField(null=False, blank=False)
    sortid = models.IntegerField(null=False, blank=False)
    question = models.ForeignKey(Question, null=False, blank=False)


class Response(models.Model):
    survey = models.ForeignKey(Survey, null=False, blank=False, related_name="responses")
    interviewee = models.ForeignKey(User, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AnswerBase(models.Model):
    question = models.ForeignKey(Question, null=False, blank=False)
    response = models.ForeignKey(Response, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AnswerText(AnswerBase):
    text = models.TextField(null=False, blank=False)


class AnswerRadio(AnswerBase):
    choice = models.ForeignKey(Choice, null=False, blank=False)


class AnswerSelect(AnswerBase):
    choice = models.ForeignKey(Choice, null=False, blank=False)


class AnswerCheck(AnswerBase):
    choice = models.ManyToManyField(Choice)


class AnswerDateTime(AnswerBase):
    choice = models.DateTimeField(null=False, blank=False)


class AnswerInteger(AnswerBase):
    choice = models.IntegerField(null=False, blank=False)









