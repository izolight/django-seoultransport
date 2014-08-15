# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busgokr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequence',
            name='direction_location',
            field=models.ForeignKey(to='busgokr.Location', null=True),
            preserve_default=True,
        ),
    ]
