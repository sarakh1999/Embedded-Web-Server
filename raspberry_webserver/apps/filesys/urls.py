"""raspberry_webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from . import views

app_name = 'filesys'
urlpatterns = [
    path('<int:dir_id>/makedir/', views.make_dir, name='make-dir'),
    path('<int:dir_id>/removedir/', views.remove_dir, name='remove-dir'),
    path('<int:dir_id>/uploadfile/', views.upload_file, name='upload-file'),
    path('<int:dir_id>/removefile/', views.remove_file, name='remove-file'),
    path('getfile/<int:file_id>/', views.get_file, name='get-file'),
    path('<int:dir_id>/', views.get_dir, name='get-dir'),
    path('', views.go_to_root, name='root'),
]
