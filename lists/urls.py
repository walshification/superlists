from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
)

urlpatterns += staticfiles_urlpatterns()
