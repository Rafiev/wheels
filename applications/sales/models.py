from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from applications.accounts.models import Team
from applications.products.models import Storage, Wheel

User = get_user_model()


class Sale(models.Model):
    created_at = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sale')
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='sale')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='sale')
    wheels = models.JSONField()


class Defect(models.Model):
    created_at = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='defect')
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='defect')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, related_name='defect')
    wheels = models.JSONField()


class Return(models.Model):
    created_at = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='returns')
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='returns')
    wheels = models.ForeignKey(Wheel, on_delete=models.CASCADE, null=True, related_name='returns')
