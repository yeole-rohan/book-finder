from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","isVerified", "email", "mobileNumber", "longitude", "latitude", "shopName", "gstn","created", "lastUpdated", "first_name", "last_name",  "username", "shopAddress")
