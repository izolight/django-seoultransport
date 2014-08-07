from django.conf.urls import patterns, url
from busgokr import views

urlpatterns = patterns('',
    url(r'^lines/$', views.all_lines),
    url(r'^lines/(.+)/$', views.search_lines),
    url(r'^stations/$', views.search_stations),
    url(r'^line/(?P<line_id>\d+)/$', views.line_detail),
    url(r'^station/(?P<station_id>\d+)/$', views.station_detail),
    url(r'^update_lines/$', views.update_lines),
    url(r'^update_segments/$', views.update_segments),
)