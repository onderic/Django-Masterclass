# Generated by Django 5.1.2 on 2024-10-14 15:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RandomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('simple_objects', models.ManyToManyField(blank=True, related_name='random_objects', to='common.simplemodel')),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('start_date__lt', models.F('end_date'))), name='start_date_before_end_date')],
            },
        ),
    ]