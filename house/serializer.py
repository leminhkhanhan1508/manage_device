from rest_framework import serializers
from .models import User,House,Room,Device

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

class change_status_device(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    device_id = serializers.CharField(max_length=100)
    status=serializers.CharField(max_length=100)

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

