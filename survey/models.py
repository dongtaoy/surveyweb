__author__ = 'dongtao'
from django.db import models
from django.contrib.auth.models import User, Permission, ContentType
from guardian.shortcuts import assign_perm
from django.utils.timezone import get_current_timezone


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


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
        assign_perm('survey.view_survey', self.creator, self)
        assign_perm('survey.change_survey', self.creator, self)
        assign_perm('survey.delete_survey', self.creator, self)

    def __unicode__(self):
        return self.name

    def get_questions(self):
        import itertools

        return list(itertools.chain.from_iterable(map(lambda p: getattr(p, 'containers').all(), self.pages.all())))

    def get_num_responses(self, days=30):
        import datetime
        import calendar
        import pytz

        data = []
        for day in reversed(range(0, days)):
            temp_date = datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(days=day)
            print self.responses.filter(created__startswith=temp_date.date())
            data.append(
                [calendar.timegm(temp_date.timetuple()) * 1000,
                 len(self.responses.filter(created__startswith=temp_date.date()))])

        return data


class Page(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, default='Add a title')
    survey = models.ForeignKey(Survey, null=False, blank=False, related_name='pages')
    order = models.IntegerField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.survey.pages.count() + 1
        super(Page, self).save(*args, **kwargs)
        assign_perm('survey.delete_page', self.survey.creator, self)
        assign_perm('survey.change_page', self.survey.creator, self)

    def __unicode__(self):
        return self.title


# class ContainerType(models.Model):
# text = models.CharField(max_length=50, null=False, blank=False)


class Container(models.Model):
    page = models.ForeignKey('Page', null=False, blank=False, related_name="containers")
    order = models.IntegerField(null=False, blank=False)
    QUESTION = 'QU'
    TEXT = 'TE'
    IMAGE = 'IM'
    STATUS_CHOICES = (
        (QUESTION, 'QUESTION'),
        (TEXT, 'TEXT'),
        (IMAGE, 'IMAGE'),
    )
    type = models.CharField(choices=STATUS_CHOICES, max_length=2, null=False, blank=False)

    class Meta:
        ordering = ['order']

    # def get_name(self):
    # pass

    def has_change_permission(self, user):
        if self.type == Container.TEXT:
            return user.has_perm('survey.change_textcontainer', self.textcontainer)
        elif self.type == Container.QUESTION:
            return user.has_perm('survey.change_questioncontainer', self.questioncontainer)
        return False

    def has_delete_permission(self, user):
        if self.type == Container.TEXT:
            return user.has_perm('survey.delete_textcontainer', self.textcontainer)
        elif self.type == Container.QUESTION:
            return user.has_perm('survey.delete_questioncontainer', self.questioncontainer)
        return False

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.page.containers.count() + 1
        super(Container, self).save(*args, **kwargs)


class ImageContainer(Container):
    image = models.ImageField(null=False, blank=False)


class TextContainer(Container):
    text = models.TextField(null=False, blank=False)
    SUCCESS = 'SU'
    DEFAULT = 'DE'
    INFORMATION = 'IN'
    WARNING = 'WA'
    DANGER = 'DA'

    CATEGORY_CHOICES = (
        (SUCCESS, 'Success'),
        (DEFAULT, 'Default'),
        (INFORMATION, 'Info'),
        (WARNING, 'Warning'),
        (DANGER, 'Danger'),
    )
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, null=False, blank=False, default=DEFAULT)

    def save(self, *args, **kwargs):
        super(TextContainer, self).save(*args, **kwargs)
        assign_perm('survey.delete_textcontainer', self.page.survey.creator, self)
        assign_perm('survey.change_textcontainer', self.page.survey.creator, self)


class QuestionType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    helper = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    icon_css = models.CharField(max_length=100, null=True, blank=True)
    MULTIPLE_CHOICE = 'MC'
    SINGLE_CHOICE = 'SC'
    TEXT = 'TE'
    ANSWERTYPE_CHOICES = (
        (MULTIPLE_CHOICE, 'MULTIPLE_CHOICE'),
        (SINGLE_CHOICE, 'SINGLE_CHOICE'),
        (TEXT, 'TEXT')
    )
    answertype = models.CharField(choices=ANSWERTYPE_CHOICES, max_length=2, null=False, blank=False, default='TE')

    class Meta:
        ordering = ['order']


    def get_name(self):
        return self.name.lower().replace(' ', '-')

    def get_edit_template_name(self):
        return "survey/question/%s.edit.html" % self.get_name()

    def get_display_template_name(self):
        return "survey/question/%s.display.html" % self.get_name()

    def __unicode__(self):
        return self.name


class QuestionContainer(Container):
    question = models.TextField(null=False, blank=False)
    questiontype = models.ForeignKey(QuestionType)
    required = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        super(QuestionContainer, self).save(*args, **kwargs)
        assign_perm('survey.delete_questioncontainer', self.page.survey.creator, self)
        assign_perm('survey.change_questioncontainer', self.page.survey.creator, self)

    def get_choices(self):
        choices = self.choices.all()
        return tuple([(choice.text, choice.text) for choice in choices])


    def __unicode__(self):
        return self.question


class Choice(models.Model):
    text = models.CharField(max_length=100, null=False, blank=False)
    order = models.IntegerField(null=False, blank=False)
    question = models.ForeignKey(QuestionContainer, null=False, blank=False, related_name='choices')

    class Meta:
        unique_together = ('text', 'question')

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.question.choices.count() + 1
        super(Choice, self).save(*args, **kwargs)


#

class EloItem(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    rating = models.FloatField(null=False, blank=False)
    question = models.ForeignKey(QuestionContainer, null=False, blank=False)


class Response(models.Model):
    survey = models.ForeignKey(Survey, null=False, blank=False, related_name="responses")
    interviewee = models.ForeignKey(User, null=False, blank=False, related_name="responses")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AnswerBase(models.Model):
    question = models.ForeignKey(QuestionContainer, null=False, blank=False, related_name="answers")
    response = models.ForeignKey(Response, null=False, blank=False, related_name="answers")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    TEXT = 'TE'
    SINGLE_CHOICE = 'SC'
    MULTIPLE_CHOICE = 'MC'
    choices = (
        (TEXT, 'TEXT'),
        (SINGLE_CHOICE, 'SINGLE_CHOICE'),
        (MULTIPLE_CHOICE, 'MULTIPLE_CHOICE'),
    )
    type = models.CharField(choices=choices, max_length=2, null=False, blank=False, default=TEXT)


class AnswerText(AnswerBase):
    text = models.TextField(null=False, blank=False)


class AnswerChoice(AnswerBase):
    choice = models.ForeignKey(Choice, null=False, blank=False, related_name='answers')


class AnswerCheck(AnswerBase):
    choices = models.ManyToManyField(Choice, related_name='checkanswers')


class AnswerElo(AnswerBase):
    item = models.ForeignKey(EloItem, null=False, blank=False)
    current_rating = models.FloatField(null=False, blank=False)





