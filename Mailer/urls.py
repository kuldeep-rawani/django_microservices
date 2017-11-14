from django.conf.urls import url
from . import MailerController

urlpatterns = [
	url(r'^', MailerController.mail),
]