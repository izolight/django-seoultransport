from django.db import models


class RouteType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class BusStation(models.Model):
    id = models.IntegerField(primary_key=True)
    arsid = models.IntegerField(unique=True, null=True)
    name = models.ForeignKey(Location, null=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, null=True)

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.id)


class Corporation(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class BusRoute(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    length = models.DecimalField(max_digits=4, decimal_places=1)
    route_type = models.ForeignKey(RouteType)
    first_time = models.DateTimeField()
    last_time = models.DateTimeField()
    first_station = models.ForeignKey('BusStation', related_name='first_station', null=True)
    last_station = models.ForeignKey('BusStation', related_name='last_station', null=True)
    interval = models.IntegerField()
    first_low_time = models.DateTimeField(null=True)
    last_low_time = models.DateTimeField(null=True)
    corporation = models.ForeignKey('Corporation')

    def __str__(self):
        return self.name


class SearchedLive(models.Model):
    busroute = models.ForeignKey(BusRoute)

    def __str__(self):
        return str(self.busroute)


class Section(models.Model):
    id = models.IntegerField(primary_key=True)
    distance = models.DecimalField(max_digits=8, decimal_places=3)
    speed = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Sequence(models.Model):
    number = models.IntegerField()
    section = models.ForeignKey('Section', null=True)
    turnstation = models.ForeignKey('BusStation', related_name='turnstation')
    station = models.ForeignKey('BusStation')
    is_turnstation = models.BooleanField(default=False)
    route = models.ForeignKey('BusRoute')
    direction = models.ForeignKey(Location, null=True)
    first_time = models.TimeField(null=True)
    last_time = models.TimeField(null=True)

    def __str__(self):
        return str(self.route) + '-' + str(self.number)