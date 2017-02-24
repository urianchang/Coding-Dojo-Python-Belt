from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^travels$', views.welcome, name="travels_home"),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.newTrip, name="travels_new"),
    url(r'^travels/add/process$', views.addTrip),
    url(r'^travels/destination/(?P<id>\d+)$', views.showTrip),
    url(r'^join$', views.joinTrip),
    url(r'^.+$', views.any)
]
