# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^create/$', views.image_create, name='create'),
]