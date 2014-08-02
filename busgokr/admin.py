from django.contrib import admin
from busgokr.models import BusStation, BusRoute, RouteType, Corporation, Section, Sequence
# Register your models here.

admin.site.register(BusRoute)
admin.site.register(RouteType)
admin.site.register(BusStation)
admin.site.register(Corporation)
admin.site.register(Sequence)
admin.site.register(Section)