from django.conf.urls import url
from django.urls import path

from ems_admin import views
urlpatterns = [
    path('login/', views.login),
    path('check/', views.check),
    path('get_captcha/', views.get_captcha),
    path('register/', views.register),
    path('insert/', views.insert),
    path('exit/', views.exit),
    url('^$', views.login),
]
