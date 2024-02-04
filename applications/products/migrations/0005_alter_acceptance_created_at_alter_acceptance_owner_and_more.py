# Generated by Django 5.0.1 on 2024-02-04 16:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('products', '0004_acceptance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptance',
            name='created_at',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='acceptance',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acceptance', to='accounts.team'),
        ),
        migrations.AlterField(
            model_name='acceptance',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acceptance', to=settings.AUTH_USER_MODEL),
        ),
    ]
