"""
URL configuration for StalkerifyHeroku project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path
from StalkerifyHeroku import settings
from StalkerifyHeroku.views import *


urlpatterns = [
    path('', index, name='index'),
    path('post_from_index/', post_from_index, name='post_from_index'),
    path('found/', found, name='found'),
    path('choose_track/', search_by_name, name='choose_track'),
    path('render_result_site/', render_result_site, name='render_result_site'),
    path('render_choose_result_site/', render_choose_result_site, name='render_choose_result_site'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
