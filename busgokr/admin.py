from django.contrib import admin
from busgokr.models import BusStation, BusRoute, RouteType
# Register your models here.

admin.site.register(BusRoute)
admin.site.register(RouteType)
admin.site.register(BusStation)