# Generated by Django 5.0.3 on 2024-03-14 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0008_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTwo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name2', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TestOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name1', models.CharField(max_length=100)),
                ('one', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.testtwo')),
            ],
        ),
    ]
