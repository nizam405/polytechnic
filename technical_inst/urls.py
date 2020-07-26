"""technical_inst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from root.views import home, about
from admission.views import admission

urlpatterns = [
    path('', home, name='home'),
    path('courses/', include('courses.urls')),
    path('admission/', include('admission.urls')),
    path('applicants/', include('applicants.urls')),
    path('students/', include('students.urls')),
    path('staffs/', include('staffs.urls')),
    path('user/', include('accounts.urls')),
    path('notices/', include('notices.urls')),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls, name='django_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
