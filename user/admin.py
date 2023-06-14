from django.contrib import admin

from user.models import User, Location

admin.site.register(User)
admin.site.register(Location)