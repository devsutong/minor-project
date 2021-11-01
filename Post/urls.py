from django.conf.urls import  url
from .views import UploadMatertialView

urlpatterns = [
    url("upload-material/", UploadMatertialView.as_view(), name="upload-material",)
]