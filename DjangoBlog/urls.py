"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views

import xadmin
from xadmin.plugins import xversion

from blog.sitemap import BlogSitemap


xversion.register_models()
xadmin.autodiscover()

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls, name='xadmin'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml/', sitemap_views.sitemap, {'sitemaps': {'blogs': BlogSitemap}}),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('comment/', include(('comment.urls', 'comment'), namespace='comment')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
