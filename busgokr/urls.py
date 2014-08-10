from django.conf.urls import patterns, url
from busgokr import views

urlpatterns = patterns('',
    url(r'^lines/$', views.all_lines),
    url(r'^lines/(.+)/$', views.search_lines),
    url(r'^locations/$', views.all_locations),
    url(r'^locations/(.+)/$', views.search_locations),
    url(r'^line/(\d+)/$', views.line_detail),
    url(r'^location/(\d+)/$', views.location_detail),
    url(r'^station/(\d+)/$', views.station_detail),
    url(r'^update_lines/$', views.update_lines),
    url(r'^update_segments/$', views.update_segments),
    url(r'^direction/(.+)/$', views.directions),
    url(r'^corporation/(\d+)/$', views.corporations),
)