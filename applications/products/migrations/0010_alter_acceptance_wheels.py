# Generated by Django 5.0.1 on 2024-02-11 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_acceptance_wheels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptance',
            name='wheels',
            field=models.JSONField(null=True),
        ),
    ]
