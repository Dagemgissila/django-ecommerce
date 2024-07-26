from django.contrib import admin
from userauthes.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=["username","email","bio"]

admin.site.register(User,UserAdmin)
