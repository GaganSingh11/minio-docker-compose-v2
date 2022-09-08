from datetime import timedelta
from minio import Minio
from rest_framework import serializers
from user.models import UserProfile, MinIO
import os

HOST = os.getenv("MINIO_HOST")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("MINIO_BUCKET")

minioClient = Minio(HOST, access_key=ACCESS_KEY, 
                    secret_key=SECRET_KEY, secure=False)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # fields = "__all__"
        fields = ["id", "username", "firstname", "lastname", "lastupload"]

class RecordSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = MinIO
        # fields = "__all__"
        fields = ["id", "filename", "path", "created"]

    def get_path(self, obj):
        filepath = minioClient.presigned_get_object(BUCKET, obj.filename, timedelta(hours=2))
        # filepath = f"http://172.19.0.2:9000/{BUCKET}/{obj.filename}"
        return filepath