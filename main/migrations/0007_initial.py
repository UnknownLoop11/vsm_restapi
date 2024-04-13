# Generated by Django 5.0.3 on 2024-03-13 18:44

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0006_remove_file_man_remove_uploadm_new_mod_delete_test_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ph', phonenumber_field.modelfields.PhoneNumberField(max_length=13, region='IN')),
            ],
        ),
    ]
