from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from applications.accounts.models import Team
from applications.products.models import Storage, Wheel, Season

User = get_user_model()


class Action(models.Model):

    class ActionType(models.TextChoices):
        SALE = 'Продажа'
        DEFECT = 'Брак'
        RETURN = 'Возврат'

    season = models.CharField(max_length=10, choices=Season.choices, default=Season.SUMMER,)
    action_type = models.CharField(max_length=10,  choices=ActionType.choices, default=ActionType.SALE, )
    created_at = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='action')
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='action')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='action')
    wheels = models.JSONField()

    def __str__(self):
        return f'{self.owner}: {self.action_type}'