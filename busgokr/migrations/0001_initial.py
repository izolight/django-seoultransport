# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusRoute',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('length', models.DecimalField(max_digits=4, decimal_places=1)),
                ('first_time', models.DateTimeField()),
                ('last_time', models.DateTimeField()),
                ('interval', models.IntegerField()),
                ('first_low_time', models.DateTimeField(null=True)),
                ('last_low_time', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BusStation',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('arsid', models.IntegerField(null=True, unique=True)),
                ('latitude', models.DecimalField(max_digits=18, null=True, decimal_places=15)),
                ('longitude', models.DecimalField(max_digits=18, null=True, decimal_places=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='busroute',
            name='last_station',
            field=models.ForeignKey(null=True, to='busgokr.BusStation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='busroute',
            name='first_station',
            field=models.ForeignKey(null=True, to='busgokr.BusStation'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='busroute',
            name='corporation',
            field=models.ForeignKey(to='busgokr.Corporation'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='busstation',
            name='name',
            field=models.ForeignKey(null=True, to='busgokr.Location'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='RouteType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='busroute',
            name='route_type',
            field=models.ForeignKey(to='busgokr.RouteType'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SearchedLive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('busroute', models.ForeignKey(to='busgokr.BusRoute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('distance', models.DecimalField(max_digits=8, decimal_places=3)),
                ('speed', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.IntegerField()),
                ('is_turnstation', models.BooleanField(default=False)),
                ('direction', models.CharField(max_length=30)),
                ('first_time', models.TimeField(null=True)),
                ('last_time', models.TimeField(null=True)),
                ('route', models.ForeignKey(to='busgokr.BusRoute')),
                ('section', models.ForeignKey(null=True, to='busgokr.Section')),
                ('station', models.ForeignKey(to='busgokr.BusStation')),
                ('turnstation', models.ForeignKey(to='busgokr.BusStation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
