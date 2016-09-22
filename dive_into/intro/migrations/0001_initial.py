# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=1000)),
                ('send_date', models.DateTimeField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.CharField(max_length=200)),
                ('loyal', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='intro.Clients', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='activities',
            name='client_id',
            field=models.ForeignKey(to='intro.Clients', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='activities',
            name='contact_id',
            field=models.ForeignKey(to='intro.Contacts', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
