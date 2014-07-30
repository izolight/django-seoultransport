from django.http import HttpResponse
from django.template import RequestContext, loader
import logging
import json

logger = logging.getLogger(__name__)

BASE_URL = 'http://m.bus.go.kr/mBus/bus'
PARAM_SEARCH_STRING = 'strSrch'
RESULT_LIST = 'resultList'

# Create your views here.
def line_search(request):
    if 'line' in request.POST:
        from busgokr import bus

        lines = bus.get_bus_lines(request.POST['line'])
    else:
        return HttpResponse('empty')
    template = loader.get_template('busgokr/lines.html')
    context = RequestContext(request, {
        'lines': lines,
    })
    return HttpResponse(template.render(context))


def index(request):
    template = loader.get_template('busgokr/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def add_to_db(request):
    if 'bus_line' in request.POST:
        from busgokr.models import BusStation, BusRoute, RouteType
        from datetime import datetime

        b = request.POST['bus_line']
        b = b.replace("\\'", 'REPLACE').replace("'", '"').replace('REPLACE', "\\'")
        line = json.loads(b)

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

        first_station, x = BusStation.objects.get_or_create(name=line[FIRST_STATION])
        last_station, x = BusStation.objects.get_or_create(name=line[LAST_STATION])

        id = int(line[BUS_LINE_ID])
        name = line[BUS_LINE_NAME]
        length = float(line[LENGTH])
        route_type = RouteType.objects.get(id=int(line[TYPE]))
        first_time = datetime.strptime(line[BUS_LINE_FIRST_TIME], '%Y%m%d%H%M%S')
        last_time = datetime.strptime(line[BUS_LINE_LAST_TIME], '%Y%m%d%H%M%S')
        interval = int(line[INTERVAL])
        if line[FIRST_LOW_TIME] == " ":
            first_low = " "
        else:
            first_low = datetime.strptime(line[FIRST_LOW_TIME], '%Y%m%d%H%M%S')
        if line[LAST_LOW_TIME] == " ":
            last_low = " "
        else:
            last_low = datetime.strptime(line[LAST_LOW_TIME], '%Y%m%d%H%M%S')
        corporation = line[CORPORATION]

        BusRoute.objects.get_or_create(id=id, name=name, length=length, route_type=route_type, first_time=first_time,
                                       last_time=last_time, first_station=first_station, last_station=last_station,
                                       interval=interval, corporation=corporation)
        return HttpResponse('success')
    else:
        return HttpResponse('empty')
