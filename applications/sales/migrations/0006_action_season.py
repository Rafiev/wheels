# Generated by Django 5.0.1 on 2024-03-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_remove_return_owner_remove_return_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='season',
            field=models.CharField(choices=[('Зима', 'Winter'), ('Лето', 'Summer')], default='Лето', max_length=4),
        ),
    ]