from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer,RecordSerializer
from user.models import UserProfile, MinIO
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from minio import Minio
import os

HOST = os.getenv("MINIO_HOST")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("MINIO_BUCKET")

minioClient = Minio(HOST, access_key=ACCESS_KEY, 
                    secret_key=SECRET_KEY, secure=False)

# @api_view(["GET"])
# def getData(request):
#     data = [
#         {"GET":"/api/v1/docs"},
#         {"GET":"/api/v1/upload"},
#     ]
#     return Response(data)

# @api_view(["post"])
# def uploader(request):
#     bucket = "vorn-sensor-data-1"
#     data = request.data
#     filename = data["filename"]
#     data.pop("filename")
#     data_bytes = json.dumps(data, indent=2).encode("utf-8")
#     result = minioClient.put_object(bucket, filename, BytesIO(data_bytes), len(data_bytes), content_type="application/json")
#     return Response(result.etag)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def fileUploader(request):
    user_id = request.user.id
    file = request.data["file"]
    path = file.temporary_file_path()

    if minioClient.bucket_exists(BUCKET):
        storage_entry = minioClient.fput_object(bucket_name=BUCKET, object_name=file.name, 
                                file_path=path, content_type="application/csv")
    else:
        minioClient.make_bucket(BUCKET)
        storage_entry = minioClient.fput_object(bucket_name=BUCKET, object_name=file.name, 
                                file_path=path, content_type="application/csv")  
                                  
    ref_record = {
        "filename": file.name,
        "user_id":user_id}  
    try:                      
        ref_entry = MinIO.objects.create(**ref_record)
        return Response({"uploaded": storage_entry.etag})
    except IntegrityError:
        return Response({"msg": "already exits"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getRecord(request):
    user_id = request.user.id
    records = MinIO.objects.filter(user_id=user_id).all()
    serializer = RecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getProfiles(request):
    profile = UserProfile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getProfile(request, pk):
    try:
        profile = UserProfile.objects.get(id=pk)
    except ValidationError:
        return Response({"msg":"Invalid uuid"}, status=400)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)