from django.contrib import admin

from applications.sales.models import Sale, Defect, Return

admin.site.register(Sale)
admin.site.register(Defect)
admin.site.register(Return)