from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import Http404
import magic
import os
import json

# sending mail
def mail(request):
	try:
		attachment_list = []
		UPLOAD_FOLDER = os.getcwd()+'/attachment/'
		sender = 'kuldeep.rawani159@gmail.com'
		body = request.POST.get('body')
		subject = request.POST.get('subject')
		receiver = request.POST.getlist('receiver')
		cc = request.POST.getlist('cc')
		bcc = request.POST.getlist('bcc')
		attachments = request.FILES.getlist('files[]')
		email = EmailMessage(subject, body, sender, receiver, bcc=bcc, cc=cc)
		for attachment in attachments:
			filename = attachment.name
			if not os.path.isdir(UPLOAD_FOLDER):
				os.mkdir(UPLOAD_FOLDER)
			file_to_be_uploaded = os.path.join(UPLOAD_FOLDER, filename)
			attachment_list.append(file_to_be_uploaded) 
			with open(file_to_be_uploaded, 'wb+') as dest:
				for chunk in attachment.chunks():
					dest.write(chunk)
		get_attachment(attachment_list, email)
		if email.send(fail_silently=False):
			if len(attachments):
				os.remove(file_to_be_uploaded)
			return HttpResponse('sent')
		return HttpResponse('not able to sent')
	except:
		raise Http404

#get MimeType	
def get_mime_type(file_to_be_uploaded):
			mime = magic.Magic(mime=True)
			mime_type = mime.from_file(file_to_be_uploaded)
			return mime_type

# get Attachment
def get_attachment(attachments, email):
	for attachment in attachments:
			open_attachment = open(attachment, 'rb')
			mime_type = get_mime_type(attachment)
			email.attach(attachment.split('/')[-1], open_attachment.read(), mime_type)	
	