from django.conf.urls import  url
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r"my-material", views.MyMaterialViewset, basename="my-material")
# router.register(r"claim-material", views.ClaimMaterialView, basename="claim-material")

urlpatterns = [
    url("upload-material/", views.UploadMatertialView.as_view(), name="upload-material",),
    url("materials/", views.MaterialListAPIView.as_view(), name="materials"),
    url("claim-material/", views.ClaimMaterialView.as_view(), name="claim-material"),
    path("", include(router.urls))
]   