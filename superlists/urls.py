from django.conf.urls import include, url
# from django.contrib import admin

from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='lists/home.html'),
    url(r'^lists/', include('lists.urls')),
    # url(r'^admin/', include(admin.site.urls)),
]
