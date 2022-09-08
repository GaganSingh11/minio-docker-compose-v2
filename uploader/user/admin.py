from django.contrib import admin

# Register your models here.
from .models import UserProfile, MinIO

admin.site.register(UserProfile)
admin.site.register(MinIO)