import os, datetime, magic, re
from werkzeug.utils import secure_filename
from env import *
from models import Uploads
import random


##
# To get current month and year
##
def getCurrentMonthAndYear():
    return datetime.date.today().strftime("%B")+datetime.date.today().strftime("%Y")

##
# Get File Name
##
def get_file_name(file):
    file_name = secure_filename(os.path.basename(file.name))
    is_exists = Uploads.objects.filter(name=file_name).count()
    if not is_exists:
        return file_name
    while is_exists:
        random_value = str(random.randint(1,100))
        file_name = file_name.split('.')
        file_name = file_name[0]+random_value+'.'+file_name[1]
        is_exists = Uploads.objects.filter(name=file_name).count()
    return file_name


##
# Get File Extension
##
def get_file_extension(file):
    return os.path.splitext(secure_filename(os.path.basename(file.name)))[1]

##
# Get File Title
##
def get_file_title(file):
    return os.path.splitext(secure_filename(os.path.basename(file.name)))[0]

##
# Get File MIME Type
##
def get_mime_type(file):
    return magic.from_file(UPLOAD_FOLDER+'/'+secure_filename(os.path.basename(file.name)), mime=True)

##
# Get File Path Where File gets uploaded on server
##
def get_file_path(file):
    return UPLOAD_FOLDER+'/'+secure_filename(os.path.basename(file.name))

##
# Get File Size in MB
##
def get_file_size(file):
    return os.path.getsize(get_file_path(file))/1024

##
# Get Allowed Extension
##
def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'doc', 'xls', 'csv']
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS