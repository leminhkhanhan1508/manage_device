from rest_framework import serializers
from .models import User,House,Room,Device,Sensor

class deviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields=["id","device_name","status",]

class roomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields=["id","room_name",]

class houseSerializer(serializers.ModelSerializer):
    class Meta:
        model=House
        fields=["id","house_name","address"]

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","user_name","password","full_name","phone_number",]

class sensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "sensor_id", "sensor_name", "value", "unit", "time", ]

class change_status_device(serializers.Serializer):
    device_id = serializers.CharField(max_length=100)
    status=serializers.BooleanField(default=True)

class get_devices(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    room_id = serializers.CharField(max_length=100)

#request getList Room
class get_rooms(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    house_id = serializers.CharField(max_length=100)

#request getList house
class get_house(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
#request Create Room
class create_room(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    room_name = serializers.CharField(max_length=100)
    house_id = serializers.CharField(max_length=100)

#request Create House
class create_house(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    house_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)

#request Create Device
class create_device(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    device_name = serializers.CharField(max_length=100)
    room_id = serializers.CharField(max_length=100)

#request login
class loginRequest(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class create_account_request(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    full_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)


class add_value_sensor_request(serializers.Serializer):
    sensor_id = serializers.CharField(max_length=100)
    house_id = serializers.CharField(max_length=100)
    sensor_name = serializers.CharField(max_length=100)
    unit = serializers.CharField(max_length=100)
    value = serializers.CharField(max_length=100)


class get_data_sensor_request(serializers.Serializer):
    house_id = serializers.CharField(max_length=100)

class get_data_sensor_date_request(serializers.Serializer):
    house_id = serializers.CharField(max_length=100)
    sensor_id = serializers.CharField(max_length=100)
    date = serializers.CharField(max_length=100)