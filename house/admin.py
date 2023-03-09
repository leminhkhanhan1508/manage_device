from django.contrib import admin
from .models import User,House,Room,Device
# Register your models here.


admin.site.register(User)
admin.site.register(House)
admin.site.register(Room)
admin.site.register(Device)