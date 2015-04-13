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
            name='ImageSubContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('container', models.ForeignKey(to='core.Container')),
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
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('container', models.ForeignKey(to='core.Container')),
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
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.Category', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextSubContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('container', models.ForeignKey(to='core.Container')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerCheck',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AnswerBase')),
            ],
            bases=('core.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerDateTime',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AnswerBase')),
                ('choice', models.DateTimeField()),
            ],
            bases=('core.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerInteger',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AnswerBase')),
                ('choice', models.IntegerField()),
            ],
            bases=('core.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerRadio',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AnswerBase')),
            ],
            bases=('core.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerSelect',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AnswerBase')),
            ],
            bases=('core.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerText',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AnswerBase')),
                ('text', models.TextField()),
            ],
            bases=('core.answerbase',),
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(to='core.Survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(to='core.QuestionType'),
        ),
        migrations.AddField(
            model_name='page',
            name='survey',
            field=models.ForeignKey(to='core.Survey'),
        ),
        migrations.AddField(
            model_name='container',
            name='page',
            field=models.ForeignKey(to='core.Page'),
        ),
        migrations.AddField(
            model_name='container',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.ContainerType', null=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='core.Question'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='question',
            field=models.ForeignKey(to='core.Question'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='response',
            field=models.ForeignKey(to='core.Response'),
        ),
        migrations.AddField(
            model_name='answerselect',
            name='choice',
            field=models.ForeignKey(to='core.Choice'),
        ),
        migrations.AddField(
            model_name='answerradio',
            name='choice',
            field=models.ForeignKey(to='core.Choice'),
        ),
        migrations.AddField(
            model_name='answercheck',
            name='choice',
            field=models.ManyToManyField(to='core.Choice'),
        ),
    ]
