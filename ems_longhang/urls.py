"""ems_longhang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.views import serve  # static

# 临时解决
# from django.conf import settings
from django.conf.urls import url
# from django.views.static import serve as static_serve  # media注意这里引入的与上面的不同
# 关闭Debug调试后解决
# def return_static(request, path, insecure=True, **kwargs):
#     return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employee.urls')),
    path('', include('ajax.urls')),
    path('', include('ems_admin.urls')),

    # 关闭Debug调试后解决
    # url(r'^static/(?P<path>.*)$', return_static, name='static'),
    # url(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]
