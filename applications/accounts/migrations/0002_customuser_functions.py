# Generated by Django 5.0.1 on 2024-03-05 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='functions',
            field=models.JSONField(null=True),
        ),
    ]
