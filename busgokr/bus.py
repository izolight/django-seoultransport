import requests

BASE_URL = 'http://m.bus.go.kr/mBus/bus'
PARAM_SEARCH_STRING = 'strSrch'
RESULT_LIST = 'resultList'

def get_bus_lines(query):
    """Get an array of bus lines containing at least 1 bus line.

    :param query: the search string
    :type query: number of the busline
    :returns: array of BusLine objects
    :rtype: BusLine object
    """
    url = BASE_URL + "/getBusRouteList.bms"
    params = {PARAM_SEARCH_STRING : query}
    r = requests.get(url, params=params).json()
    return r[RESULT_LIST]