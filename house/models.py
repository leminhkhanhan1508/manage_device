from django.db import models

# Create your models here.







class User(models.Model):
  user_name = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  full_name = models.CharField(max_length=255)
  phone_number=models.CharField(max_length=255)

class House(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
  house_name = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  status = models.BooleanField(max_length=255,default=True)

class Room(models.Model):
  house=models.ForeignKey(House,on_delete=models.CASCADE,default=0)
  room_name = models.CharField(max_length=255)


class Device(models.Model):
  room=models.ForeignKey(Room,on_delete=models.CASCADE,default=0)
  device_name = models.CharField(max_length=255)
  status = models.CharField(max_length=255)


class Sensor(models.Model):
  house = models.ForeignKey(House, on_delete=models.CASCADE, default=0)
  sensor_id = models.CharField(max_length=255)
  sensor_name = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  unit = models.CharField(max_length=255)
  time = models.CharField(max_length=255)
