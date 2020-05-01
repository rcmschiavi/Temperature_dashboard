from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class Temperature(models.Model):
    TEMPERATURE = models.DecimalField(max_digits=5,decimal_places=2)
    REGISTERED_AT = models.DateTimeField(auto_now=True)
    class Meta:
       managed = True
       db_table = 'TEMPERATURE'