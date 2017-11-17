from Uploader import Uploader
from django.http import HttpResponse
from env import * 
from werkzeug.utils import secure_filename
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import helpers
import os
import shutil
from django_microservices.BaseController import *
from django_microservices.Transformer import UploadTransformer

#upload to aws s3
def upload(request):
	if request.method == 'POST':
		if request.POST.get('category') is None:
			return respondWithError(421, 'You must provide a Category to Upload')
		files = request.FILES.getlist('files[]')
		if not len(files):
			return respondWithError(421, 'No files to Upload')
		if not os.path.isdir(UPLOAD_FOLDER):
			os.mkdir(UPLOAD_FOLDER)
		response = []
		for file in files:
			filename = secure_filename(file.name)
			if file and helpers.allowed_file(filename):
				path = default_storage.save(os.path.join(UPLOAD_FOLDER, filename), ContentFile(file.read()))
				uploader = Uploader(file, request.POST.get('category'))
				response.append(uploader.upload_to_aws())
		shutil.rmtree('testing')
		return respondWithCollection(201, response, UploadTransformer)
	return respondWithError(404, 'method not found')

# download from s3
def download(request):
	all_self_link = request.GET.get('selfLink')
	all_self_link = ast.literal_eval(all_self_link)
	if not len(all_self_link):
		return respondWithError(421, 'links required for downloading')
	for self_link in all_self_link:
		self_link = self_link.split('https://s3.amazonaws.com/')
		del self_link[0]
		self_link = self_link[0].split('/')
		bucket_name, category, file_name = self_link[0], self_link[1], self_link[2]
		import boto3
		if not os.path.isdir(UPLOAD_FOLDER):
			os.mkdir(UPLOAD_FOLDER)
		s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_ACCESS_KEY_SECRET)
		s3.download_file(bucket_name, category+'/'+file_name, UPLOAD_FOLDER+'/'+file_name)
	return respondWithSuccess(200, 'your files have been downloaded!')

# to get all self links
def get_all_self_links(request):
	if request.method == 'GET':
		category = request.GET.get('category')
		if category is not None:
			from models import Uploads
			print category, type(category)
			data = Uploads.objects.filter(category=category).values()
			return respondWithCollection(200, data, UploadTransformer)
		return respondWithError(421, 'you must provide a category')
	return respondWithError(404, 'method not found')	

