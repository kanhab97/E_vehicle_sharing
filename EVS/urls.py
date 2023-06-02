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
from django.urls import path, include
from customer import views
import manager

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('user_login/', views.user_login),
    path('corpuser_login/', views.corpuser_login),
    path('user_register/', views.user_register),
    path('corpuser_register/', views.corpuser_register),
    path('logout/', views.logout),
    path('get_vehicles_availability/', views.getVehiclesAvailability),
    path('get_booking_detail/', views.getBookingDetail),
    path('book_vehicle', views.bookVehicle),
    path('customer/return_vehicle/', views.returnVehicle),
    path('contact_us/', views.contact_us),
    path('home/', views.home),
    path('vehicles_available/', views.vehicles_available),
    path('booking/', views.bookVehicle),
    path('booking_second/', views.booking_second),
    path('booking_details/', views.booking_details),
    path('returnVehicle', views.returnVehicle),
    path('paym/', views.paym),
    path('confirmation', views.confirmation),
    path('report', views.report),
    path('vehicles_available_corp/', views.vehicles_available_corp),
    path('corp_booking_conf', views.corp_booking_conf),
    path('', include('manager.urls')),
    path('', include('employee.urls'))
]
