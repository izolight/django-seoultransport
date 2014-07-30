from django.conf.urls import patterns, url
from busgokr import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^line_search/$', views.line_search),
)