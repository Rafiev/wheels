from django.db import models
from django.contrib.auth import get_user_model

from applications.accounts.models import Team
from applications.products.models import Storage

User = get_user_model()


class Sale(models.Model):
    created_at = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sale')
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='sale')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='sale')
    wheels = models.JSONField()

    def __str__(self):
        return self.owner.title