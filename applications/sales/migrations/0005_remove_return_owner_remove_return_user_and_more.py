# Generated by Django 5.0.1 on 2024-03-03 10:28

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('products', '0013_acceptance_season'),
        ('sales', '0004_alter_defect_created_at_alter_return_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='return',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='return',
            name='user',
        ),
        migrations.RemoveField(
            model_name='return',
            name='wheels',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='storage',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='user',
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('Продажа', 'Sale'), ('Брак', 'Defect'), ('Возврат', 'Return')], default='Продажа', max_length=10)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('wheels', models.JSONField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action', to='accounts.team')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action', to='products.storage')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Defect',
        ),
        migrations.DeleteModel(
            name='Return',
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
    ]
