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

# On python anywhere I had to create the table manually, with the following command:
# CREATE TABLE TEMPERATURE (id int NOT NULL AUTO_INCREMENT, TEMPERATURE decimal(5,2), REGISTERED_AT datetime, primary key (id));
# Logged on the right database