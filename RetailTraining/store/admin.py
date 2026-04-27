from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Role)
admin.site.register(User)
admin.site.register(User_Role)
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Notification)