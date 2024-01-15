from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Storage(models.Model):
    title = models.CharField(max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title


class Wheel(models.Model):
    title = models.CharField(max_length=50)
    amount = models.PositiveIntegerField(default=0)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='wheels')

    def __str__(self):
        return self.title