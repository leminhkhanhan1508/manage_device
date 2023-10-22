from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from house.serializer import loginRequest, create_account_request, create_house, create_room, get_rooms, get_house, \
    create_device, get_devices, change_status_device, add_value_sensor_request, get_data_sensor_request, \
    get_data_sensor_date_request
from .models import User, House, Room, Device, Sensor
import hashlib
from rest_framework.exceptions import ValidationError
from .serializer import deviceSerializer, roomSerializer, houseSerializer, userSerializer, sensorSerializer
from rest_framework import generics
from django.http import JsonResponse
import requests
from datetime import datetime


class login(APIView):
    def post(seft, request):
        response_False = {
            "code": "01",
            "massage": "sai tên tài khoản hoặc mật khẩu"
        }

        mdata = loginRequest(data=request.data)
        if not mdata.is_valid():
            return response_False
        userName = mdata.data["user_name"]
        password = mdata.data["password"]
        # hash password
        md5 = hashlib.md5(password.encode())
        encryptedPassword = md5.hexdigest()
        user = User.objects.filter(user_name=userName, password=encryptedPassword).first()
        if (user == None):
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        houses = House.objects.filter(user=user)
        housesJson = houseSerializer(houses, many=True)
        response_True = {
            "code": "00",
            "house_list": housesJson.data
        }
        return Response(response_True, status=status.HTTP_200_OK)


class createDevice(APIView):
    def post(seft, request):
        response_True = {
            "code": "00",
            "massage": "Thành công"
        }
        response_False = {
            "code": "01",
            "massage": "Thông tin không hơp lệ"
        }

        mdata = create_device(data=request.data)

        if not mdata.is_valid():
            return response_False
        userName = mdata.data["user_name"]
        deviceName = mdata.data["device_name"]
        roomId = mdata.data["room_id"]
        print(roomId)
        user = User.objects.filter(user_name=userName).first()
        room = Room.objects.filter(id=int(roomId)).first()
        print(room)
        if user is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        if room is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        # device default off
        statusDevice = "off"
        Device.objects.create(room=room, device_name=deviceName, status=statusDevice)
        return Response(response_True, status=status.HTTP_200_OK)


class createRoom(APIView):
    def post(seft, request):
        response_True = {
            "code": "00",
            "massage": "Thành công"
        }
        response_False = {
            "code": "01",
            "massage": "Thông tin không hơp lệ"
        }
        mdata = create_room(data=request.data)
        if not mdata.is_valid():
            return response_False
        userName = mdata.data["user_name"]
        roomName = mdata.data["room_name"]
        house_id = mdata.data["house_id"]

        user = User.objects.filter(user_name=userName).first()
        house = House.objects.filter(id=int(house_id)).first()
        if user is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        if house is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)

        Room.objects.create(house=house, room_name=roomName)
        return Response(response_True, status=status.HTTP_200_OK)


class createHouse(APIView):
    def post(seft, request):
        response_True = {
            "code": "00",
            "massage": "Thành công"
        }
        response_False = {
            "code": "01",
            "massage": "Thông tin không hơp lệ"
        }

        mdata = create_house(data=request.data)

        if not mdata.is_valid():
            return response_False
        userName = mdata.data["user_name"]
        houseName = mdata.data["house_name"]
        address = mdata.data["address"]

        user = User.objects.filter(user_name=userName).first()

        if user is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        House.objects.create(user=user, house_name=houseName, address=address)
        return Response(response_True, status=status.HTTP_200_OK)


class createAccount(APIView):
    def post(self, request):
        # notification for client
        response_True = {
            "code": "00",
            "massage": "Thành công"
        }
        response_False = {
            "code": "01",
            "massage": "Tài khoản đã tồn tại"
        }

        response_error = {
            "code": "88",
            "massage": "Sai Thông tin"
        }

        mdata = create_account_request(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response(response_error, status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        userName = mdata.data['user_name']
        password = mdata.data['password']
        fullName = mdata.data['full_name']
        phoneNumber = mdata.data['phone_number']

        # tài khoản đã tồn tại chưa
        user = User.objects.filter(user_name=userName).first()
        if (user != None):
            return Response(response_False, status=status.HTTP_200_OK)
        # hash password for account
        md5 = hashlib.md5(password.encode())
        encryptedPassword = md5.hexdigest()
        # create new account

        User.objects.create(user_name=userName, password=encryptedPassword, full_name=fullName,
                            phone_number=phoneNumber)

        return Response(response_True, status=status.HTTP_200_OK)


class getListRoom(APIView):
    def post(seft, request):
        # notification for client

        response_False = {
            "code": "01",
            "massage": "Tài khoản đã tồn tại"
        }

        response_error = {
            "code": "88",
            "massage": "Sai Thông tin"
        }
        mdata = get_rooms(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response(response_error, status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        userName = mdata.data['user_name']
        house_id = mdata.data['house_id']
        user = User.objects.filter(user_name=userName).first()
        house = House.objects.filter(id=int(house_id)).first()
        if user is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        if house is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        rooms = Room.objects.filter(house=house)
        roomsList = roomSerializer(rooms, many=True)
        response_True = {
            "code": "00",
            "room_list": roomsList.data
        }
        return Response(response_True, status=status.HTTP_200_OK)


class getListHouse(APIView):
    def post(seft, request):
        # notification for client

        response_False = {
            "code": "01",
            "massage": "Tài khoản đã tồn tại"
        }

        response_error = {
            "code": "88",
            "massage": "Sai Thông tin"
        }
        mdata = get_house(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response(response_error, status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        userName = mdata.data['user_name']

        user = User.objects.filter(user_name=userName).first()

        if user is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)

        house = House.objects.filter(user=user)
        houseList = houseSerializer(house, many=True)
        response_True = {
            "code": "00",
            "house_list": houseList.data
        }
        return Response(response_True, status=status.HTTP_200_OK)


class getListDevice(APIView):
    def post(seft, request):
        # notification for client

        response_False = {
            "code": "01",
            "massage": "Tài khoản đã tồn tại"
        }

        response_error = {
            "code": "88",
            "massage": "Sai Thông tin"
        }
        mdata = get_devices(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response(response_error, status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        userName = mdata.data['user_name']
        roomId = mdata.data['room_id']

        user = User.objects.filter(user_name=userName).first()
        room = Room.objects.filter(id=int(roomId)).first()
        if user is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        if room is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)

        device = Device.objects.filter(room=room)
        deviceList = deviceSerializer(device, many=True)
        response_True = {
            "code": "00",
            "device_list": deviceList.data
        }
        return Response(response_True, status=status.HTTP_200_OK)


class changeStatusDevice(APIView):
    def post(seft, request):
        # notification for client
        response_True = {
            "code": "00",
            "massage": "Thành công"
        }
        response_False = {
            "code": "01",
            "massage": "Thông tin không hợp lệ"
        }

        response_error = {
            "code": "88",
            "massage": "Sai Thông tin"
        }
        mdata = change_status_device(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response(response_error, status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        userName = mdata.data['user_name']
        device_id = mdata.data['device_id']
        mStatus = mdata.data['status']
        user = User.objects.filter(user_name=userName).first()
        device = Device.objects.filter(id=int(device_id)).first()
        if user is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        if device is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        # status on or off use to control device in house
        # if(turn_off_device(device_ip="<ESP32_IP_ADDRESS>")==200):
        #     device.status=mStatus
        #     device.save()
        #     return Response(response_True,status=status.HTTP_200_OK)

        return Response(response_error, status=status.HTTP_200_OK)


def turn_off_device(device_ip):
    # Send HTTP request to ESP32 to turn off the device
    url = 'http://${device_ip}/turn-off'
    response = requests.get(url)

    # Check if the command was successful
    return response.status_code


def turn_on_device():
    # Send HTTP request to ESP32 to turn off the device
    url = 'http://<ESP32_IP_ADDRESS>/turn-on'
    response = requests.get(url)

    # Check if the command was successful
    return response.status_code


class addSensorValue(APIView):
    def post(seft, request):
        response_True = {
            "code": "00",
            "massage": "Thành công"
        }
        response_False = {
            "code": "01",
            "massage": "Thông tin không hơp lệ"
        }
        mdata = add_value_sensor_request(data=request.data)

        if not mdata.is_valid():
            return response_False
        house_id = mdata.data["house_id"]
        sensor_id = mdata.data["sensor_id"]
        sensor_name = mdata.data["sensor_name"]
        value = mdata.data["value"]
        unit = mdata.data["unit"]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        house = House.objects.filter(id=int(house_id)).first()
        if house is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        Sensor.objects.create(house=house, sensor_id=sensor_id, sensor_name=sensor_name, value=value, unit=unit,
                              time=dt_string)
        return Response(response_True, status=status.HTTP_200_OK)


class getListSensor(APIView):
    def post(seft, request):
        # notification for client

        response_False = {
            "code": "01",
            "massage": "Thông tin không hợp lệ"
        }

        response_error = {
            "code": "88",
            "massage": "Thông tin không hợp lệ"
        }
        mdata = get_data_sensor_request(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response(response_error, status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        house_id = mdata.data['house_id']
        house = House.objects.filter(id=int(house_id)).first()
        if house is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)

        sensor = Sensor.objects.filter(house=house)
        final_sensor_values = []
        soilMoistureSensor = sensor.filter(sensor_id="1").last()
        temperatureSensor = sensor.filter(sensor_id="2").last()
        lightSensor = sensor.filter(sensor_id="3").last()
        rainfallSensor = sensor.filter(sensor_id="4").last()
        humiditySensor = sensor.filter(sensor_id="5").last()

        if soilMoistureSensor is not None:
            final_sensor_values.append(soilMoistureSensor)
        if temperatureSensor is not None:
            final_sensor_values.append(temperatureSensor)
        if humiditySensor is not None:
            final_sensor_values.append(humiditySensor)
        if lightSensor is not None:
            final_sensor_values.append(lightSensor)
        if rainfallSensor is not None:
            final_sensor_values.append(rainfallSensor)
        if humiditySensor is not None:
            final_sensor_values.append(humiditySensor)
        sensorList = sensorSerializer(final_sensor_values, many=True)
        response_True = {
            "code": "00",
            "sensor_list": sensorList.data
        }
        return Response(response_True, status=status.HTTP_200_OK)


class getListSensorOfDate(APIView):
    def post(seft, request):
        # notification for client

        response_False = {
            "code": "01",
            "massage": "Thông tin không hợp lệ"
        }

        response_error = {
            "code": "88",
            "massage": "Thông tin không hợp lệ"
        }
        mdata = get_data_sensor_date_request(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response(response_error, status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        house_id = mdata.data['house_id']
        sensor_id = mdata.data['sensor_id']
        date_string = mdata.data['date']
        house = House.objects.filter(id=int(house_id)).first()
        if house is None:
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        date_format = "%d/%m/%Y"
        try:
            date = datetime.strptime(date_string, date_format)
            print(date)
        except ValueError:
            print("Invalid date format")
        sensor = Sensor.objects.filter(house=house,sensor_id = sensor_id)
        data_of_date = sensor.filter(time__date=date_string)

        sensorList = sensorSerializer(sensor, many=True)
        response_True = {
            "code": "00",
            "sensor_list": data_of_date.data
        }
        return Response(response_True, status=status.HTTP_200_OK)
