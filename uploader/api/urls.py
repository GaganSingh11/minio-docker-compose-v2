from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path("api/", views.getData),
    # path("api/v1/json", views.uploader),
    
    path("api/v1/profiles", views.getProfiles),
    path("api/v1/profiles/<str:pk>", views.getProfile),

    path("api/v1/file", views.fileUploader),
    path("api/v1/records", views.getRecord),
]