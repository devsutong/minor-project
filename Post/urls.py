from django.conf.urls import  url
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register("mymaterial", views.MyMaterialViewset, basename="mymaterial")

urlpatterns = [
    url("upload-material/", views.UploadMatertialView.as_view(), name="uploadmaterial",),
    url("materials/", views.MaterialListAPIView.as_view(), name="materials"),
    url("unlockmaterial/", views.UnlockMaterialView.as_view(), name="unlockmaterial"),
    path('mymaterial/', views.MyMaterialViewset.as_view()),
    path("", include(router.urls))
]   