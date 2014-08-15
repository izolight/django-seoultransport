# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busgokr', '0003_remove_sequence_direction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sequence',
            old_name='direction_location',
            new_name='direction',
        ),
    ]
