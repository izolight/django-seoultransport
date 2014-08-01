import logging

from django.http import HttpResponse

from django.template import RequestContext, loader

from busgokr.models import BusRoute, SearchedLive
from busgokr.utils import search_live, add_line_to_db


logger = logging.getLogger(__name__)

RESULT_LIST = 'resultList'


def index(request):
    logger.error(request.path)
    template = loader.get_template('busgokr/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def search_lines(request):
    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            lines = BusRoute.objects.filter(name__contains=search)
            searched_before = len(SearchedLive.objects.filter(busroute=search))
            logger.error(searched_before)
            context = RequestContext(request, {
                'lines': lines,
                'search': search,
                'searched_before': searched_before,
            })
        elif 'live' in request.POST:
            search = request.POST['live']
            live_lines = search_live(search)
            if RESULT_LIST in live_lines:
                live_lines = live_lines[RESULT_LIST]
                for line in live_lines:
                    add_line_to_db(line)
            lines = BusRoute.objects.filter(name__contains=search)
            SearchedLive(busroute=search).save()
            context = RequestContext(request, {
                'lines': lines,
                'search': search,
            })
    elif request.method == 'GET':
        lines = BusRoute.objects.all()
        context = RequestContext(request, {
            'lines': lines,
        })

    template = loader.get_template('busgokr/lines_all.html')

    return HttpResponse(template.render(context))


def line_detail(request, line_id):
    line = BusRoute.objects.get(id=line_id)
    template = loader.get_template('busgokr/line.html')
    context = RequestContext(request, {
        'line': line,
    })
    return HttpResponse(template.render(context))
