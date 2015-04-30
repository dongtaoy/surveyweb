# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('sortid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sortid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('helper', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('interviewee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'DR', max_length=2, choices=[(b'OP', b'OPEN'), (b'CL', b'CLOSED'), (b'DR', b'DRAFT')])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='survey.Category', null=True)),
                ('creator', models.ForeignKey(related_name='surveys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_survey', 'Can view survey'),),
            },
        ),
        migrations.CreateModel(
            name='AnswerCheck',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerRadio',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerSelect',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerText',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
                ('text', models.TextField()),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='ImageContainer',
            fields=[
                ('container_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.Container')),
                ('image', models.ImageField(upload_to=b'')),
            ],
            bases=('survey.container',),
        ),
        migrations.CreateModel(
            name='QuestionContainer',
            fields=[
                ('container_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.Container')),
                ('question', models.TextField()),
                ('questiontype', models.ForeignKey(to='survey.QuestionType')),
            ],
            bases=('survey.container',),
        ),
        migrations.CreateModel(
            name='TextContainer',
            fields=[
                ('container_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.Container')),
                ('text', models.TextField()),
            ],
            bases=('survey.container',),
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(related_name='responses', to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='page',
            name='survey',
            field=models.ForeignKey(related_name='pages', to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='container',
            name='containtertype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='survey.ContainerType', null=True),
        ),
        migrations.AddField(
            model_name='container',
            name='page',
            field=models.ForeignKey(related_name='containers', to='survey.Page'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='response',
            field=models.ForeignKey(to='survey.Response'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='survey.QuestionContainer'),
        ),
        migrations.AddField(
            model_name='answerselect',
            name='choice',
            field=models.ForeignKey(to='survey.Choice'),
        ),
        migrations.AddField(
            model_name='answerradio',
            name='choice',
            field=models.ForeignKey(to='survey.Choice'),
        ),
        migrations.AddField(
            model_name='answercheck',
            name='choice',
            field=models.ManyToManyField(to='survey.Choice'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='question',
            field=models.ForeignKey(to='survey.QuestionContainer'),
        ),
    ]
