"""iblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from . import views

import xadmin
from xadmin.plugins import xversion

xversion.register_models()
xadmin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls, name='xadmin'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path('likes/', include(('likes.urls', 'likes'), namespace='likes')),
    path('blogs/', include(('blogs.urls', 'blogs'), namespace='blogs')),
    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('index/', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
