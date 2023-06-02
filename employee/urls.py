from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('employee/', views.index, name='index'),
    path('operator_login/',views.operator_login,name='operator_login'),
    path('operator/',views.operatordashboard,name='operator'),
    path('repair/',views.repair,name='repair'),
    path('recharge/',views.recharge,name='recharge'),
    path('repair/repairVehicle/',views.repairVehicle,name='repairVehicle'),
    path('recharge/rechargeVehicle/',views.rechargeVehicle,name='rechargeVehicle'),
    path('move/',views.move,name='move'),
    path('track/',views.track,name='track'),
    path('logoutop/',views.logoutop,name='logoutop')
]
