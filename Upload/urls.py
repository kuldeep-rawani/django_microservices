from django.conf.urls import url
from . import UploadController

urlpatterns = [
	url(r'^links', UploadController.get_all_self_links),
	url(r'^download', UploadController.download),
	url(r'^', UploadController.upload),
]