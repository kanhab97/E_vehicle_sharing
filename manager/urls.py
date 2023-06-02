"""EVS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from manager.views import employee_download, user_download
from manager import views

urlpatterns = [
    path('manager_login/', views.manager_login),
    path('employee_data/', views.employee_data, name='employee_data'),
    path('daily_report/', views.daily_reports, name='context'),
    path('user_data/', views.user_data, name='user_data'),
    path('employee_download/', views.employee_download),
    path('user_download/', views.user_download),
    path('vehicle_report_download/', views.vehicle_report_download),
    path('car_bike_report_download/', views.car_bike_report_download),
    path('pick_up_report_download/', views.pick_up_report_download),
    path('drop_report_download/', views.drop_report_download),
    path('manager_logout/', views.manager_logout),
    path('add_employee/', views.add_employee),
    path('add_vehicle/', views.add_vehicle)
]
