# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db import models
import datetime
import uuid
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Uploads(models.Model):
	id = models.CharField(max_length=255, default=uuid.uuid4, primary_key=True)
	self_link = models.CharField(max_length=255, null=True)
	name = models.CharField(max_length=255, null=True)
	is_public = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True)
	category = models.CharField(max_length=200, null=True)

	class Meta:
	    db_table = 'uploads'
