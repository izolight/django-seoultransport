from django.conf.urls import patterns, url
from busgokr import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^lines/$', views.search_lines),
    url(r'^lines/(?P<line_id>\d+)/$', views.line_detail),
)