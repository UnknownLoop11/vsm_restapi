# Generated by Django 5.0.3 on 2024-03-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_customer_reference_id_alter_file_file_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(decimal_places=16, max_digits=20),
        ),
        migrations.AlterField(
            model_name='location',
            name='long',
            field=models.DecimalField(decimal_places=16, max_digits=20),
        ),
    ]
