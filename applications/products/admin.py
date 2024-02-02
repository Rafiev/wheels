from django.contrib import admin
from .models import Storage, Wheel, Acceptance

admin.site.register(Storage)
admin.site.register(Wheel)
admin.site.register(Acceptance)