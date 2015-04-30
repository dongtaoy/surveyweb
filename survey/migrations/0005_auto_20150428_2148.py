# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_page_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questiontype',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='container',
            old_name='sortid',
            new_name='order',
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(default=b'Add a title', max_length=50),
        ),
    ]
