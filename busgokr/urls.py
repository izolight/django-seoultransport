from django.conf.urls import patterns, url
from busgokr import views

urlpatterns = patterns('',
    url(r'^lines/$', views.all_lines),
    url(r'^lines/(.+)/$', views.search_lines),
    url(r'^stations/$', views.search_stations),
    url(r'^line/(?P<line_id>\d+)/$', views.line_detail),
    url(r'^stations/(?P<station_name>.+)/$', views.station_detail),
)