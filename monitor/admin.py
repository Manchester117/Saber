from django.contrib import admin
from monitor.models import Aggregate, Report, Item, Case, Item_Error, Response_Status

# Register your models here.

admin.site.register(Aggregate)
admin.site.register(Report)
admin.site.register(Item)
admin.site.register(Item_Error)
admin.site.register(Response_Status)
admin.site.register(Case)
