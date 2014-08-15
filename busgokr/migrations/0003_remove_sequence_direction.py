# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busgokr', '0002_sequence_direction_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sequence',
            name='direction',
        ),
    ]
