from django.contrib import admin

from carpool_matcher.models import Location, Distance, Driver, Passenger, Route

# Register your models here.


class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)

class DistanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Distance, DistanceAdmin)

class DriverAdmin(admin.ModelAdmin):
    pass
admin.site.register(Driver, DriverAdmin)

class PassengerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Passenger, PassengerAdmin)

class RouteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Route, RouteAdmin)