"""
URL configuration for analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from app_analysis.views import home, upload, file_detail, deletefile, updatefile, keyword,qvsk,qvsk_analysis,kvsk_analysis,kvsk


urlpatterns = [
    path('',home, name="home"),
    path('admin/', admin.site.urls),
    path('home/' ,home, name="home"),
    path("upload/", upload, name="upload"),
    path("<str:pk>/", file_detail, name="file_detail"),
    path("delete-file/<str:pk>", deletefile, name="delete-file"),
    path("updatefile/<str:pk>", updatefile, name="updatefile"),
    path("keyword", keyword, name="keyword"),
    path("qvsk",qvsk,name="qvsk"),
    path('qvsk_analysis', qvsk_analysis, name='qvsk_analysis'),
    path("kvsk",kvsk,name="kvsk"),
    path('kvsk_analysis', kvsk_analysis, name='kvsk_analysis'),
]
