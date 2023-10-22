from django.urls import path
from . import views

urlpatterns = [
    path('create/user/', views.createAccount.as_view()),
    path('login/', views.login.as_view()),
    path("create/house/", views.createHouse.as_view()),
    path("create/room/", views.createRoom.as_view()),
    path("create/device/", views.createDevice.as_view()),
    path("house/room/", views.getListRoom.as_view()),
    path("house/", views.getListHouse.as_view()),
    path("house/room/device", views.getListDevice.as_view()),
    path("house/room/device/change", views.changeStatusDevice.as_view()),
    path("house/sensor/add/", views.addSensorValue.as_view()),
    path("house/sensor/", views.getListSensor.as_view()),
    path("house/sensor/date", views.getListSensorOfDate.as_view()),
]