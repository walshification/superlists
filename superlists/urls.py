from django.conf.urls import include, url

from lists import views

# from django.contrib import admin


urlpatterns = [
    url(r"^$", views.home_page, name="homepage"),
    url(r"^lists/", include("lists.urls")),
    # url(r'^admin/', include(admin.site.urls)),
]
