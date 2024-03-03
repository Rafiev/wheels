# Generated by Django 5.0.1 on 2024-03-03 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_acceptance_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptance',
            name='season',
            field=models.CharField(choices=[('Зима', 'Winter'), ('Лето', 'Summer')], default='Лето', max_length=4),
        ),
    ]
