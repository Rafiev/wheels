from django.db import models
from django.contrib.auth import get_user_model
from applications.accounts.models import Team

User = get_user_model()


class Storage(models.Model):
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='storages')
    title = models.CharField(max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title


class Wheel(models.Model):
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='wheels')
    title = models.CharField(max_length=50)
    amount = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='wheels')

    def __str__(self):
        return self.title


class Acceptance(models.Model):
    created_at = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='acceptance')
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='acceptance')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='acceptance')
    wheels = models.JSONField(null=True)

    def __str__(self):
        return self.owner.title
