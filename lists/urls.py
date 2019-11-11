from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.contrib import admin

from lists import views

urlpatterns = [
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^new$', views.new_list, name='new_list'),
]

urlpatterns += staticfiles_urlpatterns()
