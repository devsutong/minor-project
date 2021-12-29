<<<<<<< HEAD
from django.conf.urls import  url
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register(r"uploads", views.UploadsListAPIView, basename="my-material")
# router.register(r"claim-material", views.ClaimMaterialView, basename="claim-material")

urlpatterns = [
    url(r"upload/material/", views.UploadMatertialView.as_view(), name="upload-material",),
    url(r"materials/", views.MaterialListAPIView.as_view(), name="materials"),
    url(r"unlock/material/", views.UnlockMaterialView.as_view(), name="unlock-material"),
    url(r'upvote/', views.UpVoteAPIView.as_view(), name='upvote'),
    url(r'downvote/', views.DownVoteAPIView.as_view(), name='downvote'),
    url(r"uploads", views.UploadsListAPIView.as_view(), name="uploads"),
    url(r'materialcontent', views.MaterialContentAPIView.as_view()),
    url(r'unlocks', views.UnlockedMaterialsAPIView.as_view())
    # path("", include(router.urls))
=======
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
>>>>>>> chat
]   