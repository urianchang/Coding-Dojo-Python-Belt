from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^travels$', views.welcome),
    url(r'^logout$', views.logout),
    # url(r'^delete$', views.delete),
    url(r'^.+$', views.any)
]
