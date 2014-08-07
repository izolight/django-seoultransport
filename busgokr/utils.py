from datetime import datetime
import requests
from busgokr.models import BusStation, RouteType, BusRoute, Corporation, Location, Section, Sequence
from django.utils.http import urlquote
import logging

BASE_URL = 'http://m.bus.go.kr/mBus/bus'
PARAM_SEARCH_ROUTE = 'strSrch'
PARAM_SEARCH_STATION = 'stSrch'
BUS_LINE_ID = 'busRouteId'
BUS_LINE_NAME = 'busRouteNm'
LENGTH = 'length'
TYPE = 'routeType'
BUS_LINE_FIRST_TIME = 'firstBusTm'
BUS_LINE_LAST_TIME = 'lastBusTm'
FIRST_STATION = 'stStationNm'
LAST_STATION = 'edStationNm'
INTERVAL = 'term'
FIRST_LOW_TIME = 'firstLowTm'
LAST_LOW_TIME = 'lastLowTm'
CORPORATION = 'corpNm'
STATION_ID = 'station'
ARS_ID = 'arsId'
STATION_NAME = 'stationNm'
LATITUDE = 'gpsY'
LONGITUDE = 'gpsX'
SECTION_ID = 'section'
DISTANCE = 'fullSectDist'
SPEED = 'sectSpd'
SEQUENCE_NUMBER = 'seq'
TURNSTATION_ID = 'trnstnid'
IS_TURNSTATION = 'transYn'
DIRECTION = 'direction'
SEQUENCE_FIRST_TIME = 'beginTm'
SEQUENCE_LAST_TIME = 'lastTm'

logger = logging.getLogger(__name__)


def search_bus_live(search):
    url = BASE_URL + "/getBusRouteList.bms"
    params = {PARAM_SEARCH_ROUTE: search}
    return requests.get(url, params=params).json()


def search_stations_live(search):
    url = BASE_URL + "/getSearchByName.bms"
    params = {PARAM_SEARCH_STATION: urlquote(search)}
    return requests.get(url, params=params).json()


def get_stations_by_line(line_id):
    url = BASE_URL + "/getStaionByRoute.bms"
    params = {BUS_LINE_ID: line_id}
    return requests.get(url, params=params).json()


def add_station_to_db(station):
    station_id = station[STATION_ID]
    arsid = station[ARS_ID]
    if arsid == ' ' or arsid == '0':
        arsid = None
    location_name = station[STATION_NAME]
    latitude = station[LATITUDE]
    longitude = station[LONGITUDE]

    name, x = Location.objects.get_or_create(name=location_name)

    try:
        bus_station = BusStation.objects.get(id=station_id)
    except BusStation.DoesNotExist:
        bus_station = BusStation(id=station_id, name=name, arsid=arsid, latitude=latitude, longitude=longitude)
        bus_station.save()
        return bus_station

    bus_station.name = name
    bus_station.arsid = arsid
    bus_station.latitude = latitude
    bus_station.longitude = longitude
    bus_station.save()
    return bus_station


def add_section_to_db(section):
    section_id = section[SECTION_ID]
    distance = section[DISTANCE]
    speed = section[SPEED]

    try:
        new_section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        new_section = Section(id=section_id, distance=distance, speed=speed)
        new_section.save()
    return new_section


def add_sequence_to_db(sequence, section, station):
    sequence_number = sequence[SEQUENCE_NUMBER]
    turnstation, x = BusStation.objects.get_or_create(id=sequence[TURNSTATION_ID])
    route = BusRoute.objects.get(id=sequence[BUS_LINE_ID])
    direction, x = Location.objects.get_or_create(name=sequence[DIRECTION])
    first_time = sequence[SEQUENCE_FIRST_TIME]
    last_time = sequence[SEQUENCE_LAST_TIME]

    if first_time == ':' or first_time == '  :  ':
        first_time = None
    if last_time == ':'or last_time == '  :  ':
        last_time = None

    if sequence_number == '1':
        route.first_station = station
        route.save()

    is_turnstation = False
    if sequence[IS_TURNSTATION] == 'Y':
        is_turnstation = True
        route.last_station = station
        route.save()

    try:
        Sequence.objects.get(number=sequence_number, route=route)
    except Sequence.DoesNotExist:
        sequence = Sequence(number=sequence_number, section=section, turnstation=turnstation, station=station,
                            is_turnstation=is_turnstation, route=route, direction=direction, first_time=first_time,
                            last_time=last_time)
        sequence.save()


def add_segment_to_db(segment):
    station = add_station_to_db(segment)
    section = None
    if int(segment[SECTION_ID]):
        section = add_section_to_db(segment)

    add_sequence_to_db(segment, section, station)


def add_line_to_db(line):
    id = line[BUS_LINE_ID]
    name = line[BUS_LINE_NAME]
    length = line[LENGTH]
    route_type = RouteType.objects.get(id=line[TYPE])
    first_time = datetime.strptime(line[BUS_LINE_FIRST_TIME], '%Y%m%d%H%M%S')
    last_time = datetime.strptime(line[BUS_LINE_LAST_TIME], '%Y%m%d%H%M%S')
    interval = line[INTERVAL]
    if not line[FIRST_LOW_TIME] == " ":
        first_low = datetime.strptime(line[FIRST_LOW_TIME], '%Y%m%d%H%M%S')
    else:
        first_low = None
    if not line[LAST_LOW_TIME] == " ":
        last_low = datetime.strptime(line[LAST_LOW_TIME], '%Y%m%d%H%M%S')
    else:
        last_low = None

    corporation, x = Corporation.objects.get_or_create(name=line[CORPORATION])

    try:
        BusRoute.objects.get(id=id)
    except BusRoute.DoesNotExist:
        obj = BusRoute(id=id, name=name, length=length, route_type=route_type, first_time=first_time,
                       last_time=last_time,
                       interval=interval, first_low_time=first_low, last_low_time=last_low,
                       corporation=corporation)
        obj.save()