# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20150428_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questiontype',
            name='icon_css',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
