"""Saber_VIK_WEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# Django解决Specifying a namespace in include() without providing an app_name的问题
# 需要使用include(('monitor.urls', 'monitor'), namespace='monitor'))
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^monitor/', include(('monitor.urls', 'monitor'), namespace='monitor'))
]
