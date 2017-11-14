import os.path, sys
import boto3
import helpers
from env import *
from boto3.s3.transfer import S3Transfer
from django.http import HttpResponse
from models import Uploads
import uuid

##
# Uploads To AWS
##
class Uploader():

	def __init__(self, file, category):
		self.file = file
		self.s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_ACCESS_KEY_SECRET)
		self.bucket_name = AWS_BUCKET
		self.upload_folder = UPLOAD_FOLDER
		self.bucket_directory = 'thanksgiving'
	def upload_to_aws(self):
		file_detail = self.get_file_detail()
		upload = self.upload(file_detail)
		file_detail['self_link'] = self.generate_self_link(file_detail)
		data = {}
		data['id'] = uuid.uuid4()
		data['name'] = file_detail['name']
		data['self_link'] = file_detail['self_link']
		data['category'] = self.bucket_directory
		Uploads.objects.create(**data)
		return file_detail

	def get_file_detail(self):
		return {
			'name' : helpers.get_file_name(self.file),
			'extension': helpers.get_file_extension(self.file),
			'title' : helpers.get_file_title(self.file),
			'mime_type' : helpers.get_mime_type(self.file),
			'file_path' : helpers.get_file_path(self.file),
			'size' : helpers.get_file_size(self.file)
		}

	def upload(self, file_detail): 
		self.s3.upload_file(file_detail['file_path'], self.bucket_name, self.bucket_directory+'/'+file_detail['name'],ExtraArgs = {
                'ACL': 'public-read', 
                'ContentType': file_detail['mime_type'], 
                'ContentDisposition': 'inline'
            })

	def generate_self_link(self, file_detail):
		selfLink = "https://s3.amazonaws.com/{0}/{1}/{2}".format(self.bucket_name, self.bucket_directory, file_detail['name'])
		return selfLink

	def download_from_s3(self):
		return self.s3.download_file(self.bucket_name, 'November2017/SunNov1207364620171510472206223.jpeg', '/home/kuldeep/Desktop/hello.jpeg')