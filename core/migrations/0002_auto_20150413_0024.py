# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(related_name='responses', to='core.Survey'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Category', null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='creator',
            field=models.ForeignKey(related_name='surveys', to=settings.AUTH_USER_MODEL),
        ),
    ]
