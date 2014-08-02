from django.db import models


class RouteType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class BusStation(models.Model):
    station = models.IntegerField(unique=True, null=True)
    arsid = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=17, decimal_places=15, null=True)
    longitude = models.DecimalField(max_digits=17, decimal_places=15, null=True)

    def __str__(self):
        return self.name


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
    first_station = models.ForeignKey('BusStation', related_name='first_station')
    last_station = models.ForeignKey('BusStation', related_name='last_station')
    interval = models.IntegerField()
    first_low_time = models.DateTimeField(null=True)
    last_low_time = models.DateTimeField(null=True)
    corporation = models.ForeignKey('Corporation')

    def __str__(self):
        return self.name


class SearchedLive(models.Model):
    busroute = models.CharField(max_length=10)


class Section(models.Model):
    id = models.IntegerField(primary_key=True)
    station = models.ForeignKey('BusStation', to_field='station')
    distance = models.DecimalField(max_digits=8, decimal_places=3)
    speed = models.IntegerField()


class Sequence(models.Model):
    number = models.IntegerField()
    section = models.ForeignKey('Section')
    turnstation = models.ForeignKey('BusStation', to_field='station')
    is_turnstation = models.BooleanField(default=False)
    route = models.ForeignKey('BusRoute')
    direction = models.CharField(max_length=30)
    first_time = models.DateTimeField()
    last_time = models.DateTimeField()