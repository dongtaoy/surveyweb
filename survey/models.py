__author__ = 'dongtao'
from django.db import models
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm


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
    OPEN = 'OP'
    CLOSED = 'CL'
    DRAFT = 'DR'
    STATUS_CHOICES = (
        (OPEN, 'OPEN'),
        (CLOSED, 'CLOSED'),
        (DRAFT, 'DRAFT'),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=2, null=False, blank=False, default=DRAFT)

    class Meta:
        permissions = (
            ('view_survey', 'Can view survey'),
        )

    def save(self, *args, **kwargs):
        super(Survey, self).save(*args, **kwargs)
        assign_perm('view_survey', self.creator, self)
        assign_perm('change_survey', self.creator, self)
        assign_perm('delete_survey', self.creator, self)


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
    containtertype = models.ForeignKey(ContainerType, null=True,  on_delete=models.SET_NULL)


class ImageContainer(Container):
    image = models.ImageField(null=False, blank=False)


class TextContainer(Container):
    text = models.TextField(null=False, blank=False)


class QuestionType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    helper = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    icon_css = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class QuestionContainer(Container):
    question = models.TextField(null=False, blank=False)
    questiontype = models.ForeignKey(QuestionType)


class Choice(models.Model):
    text = models.TextField(null=False, blank=False)
    sortid = models.IntegerField(null=False, blank=False)
    question = models.ForeignKey(QuestionContainer, null=False, blank=False)


class Response(models.Model):
    survey = models.ForeignKey(Survey, null=False, blank=False, related_name="responses")
    interviewee = models.ForeignKey(User, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AnswerBase(models.Model):
    question = models.ForeignKey(QuestionContainer, null=False, blank=False)
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

#
# class AnswerDateTime(AnswerBase):
#     choice = models.DateTimeField(null=False, blank=False)
#
#
# class AnswerInteger(AnswerBase):
#     choice = models.IntegerField(null=False, blank=False)

#
#
# Community
# Customer Feedback
# Demographics
# Education
# Events
# Healthcare
# Human Resources
# Industry Specific
# Just for Fun
# Market Research
# Non-Profit
# Political
# Other








