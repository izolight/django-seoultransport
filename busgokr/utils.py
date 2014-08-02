from datetime import datetime
import requests
from busgokr.models import BusStation, RouteType, BusRoute

BASE_URL = 'http://m.bus.go.kr/mBus/bus'
PARAM_SEARCH_STRING = 'strSrch'
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


def search_live(search):
    url = BASE_URL + "/getBusRouteList.bms"
    params = {PARAM_SEARCH_STRING: search}
    return requests.get(url, params=params).json()


def get_stations_by_line(line_id):
    url = BASE_URL + "/getStaionByRoute.bms"
    params = {BUS_LINE_ID: line_id}
    return requests.get(url, params=params).json()


def add_line_to_db(line):
    first_station, x = BusStation.objects.get_or_create(name=line[FIRST_STATION])
    last_station, x = BusStation.objects.get_or_create(name=line[LAST_STATION])

    id = int(line[BUS_LINE_ID])
    name = line[BUS_LINE_NAME]
    length = float(line[LENGTH])
    route_type = RouteType.objects.get(id=int(line[TYPE]))
    first_time = datetime.strptime(line[BUS_LINE_FIRST_TIME], '%Y%m%d%H%M%S')
    last_time = datetime.strptime(line[BUS_LINE_LAST_TIME], '%Y%m%d%H%M%S')
    interval = int(line[INTERVAL])
    if not line[FIRST_LOW_TIME] == " ":
        first_low = datetime.strptime(line[FIRST_LOW_TIME], '%Y%m%d%H%M%S')
    else:
        first_low = None
    if not line[LAST_LOW_TIME] == " ":
        last_low = datetime.strptime(line[LAST_LOW_TIME], '%Y%m%d%H%M%S')
    else:
        last_low = None
    corporation = line[CORPORATION]

    try:
        BusRoute.objects.get(id=id)
    except BusRoute.DoesNotExist:
        obj = BusRoute(id=id, name=name, length=length, route_type=route_type, first_time=first_time,
                       last_time=last_time, first_station=first_station, last_station=last_station,
                       interval=interval, first_low_time=first_low, last_low_time=last_low,
                       corporation=corporation)
        obj.save()