from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    lastupload = models.DateTimeField()

    def __str__(self):
        return str(self.user.username)


class MinIO(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    filename = models.CharField(max_length=200, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.filename)