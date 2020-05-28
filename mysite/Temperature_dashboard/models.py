from django.db import models
# Create your models here.

class Temperature(models.Model):
    TEMPERATURE = models.DecimalField(max_digits=5,decimal_places=2)
    REGISTERED_AT = models.DateTimeField(auto_now=True)
    TEMPERATURE_OBSERVATORY = models.DecimalField(max_digits=5,decimal_places=2)
    TIME_OBSERVATORY = models.DateTimeField(auto_now=False)
    class Meta:
       managed = True
       db_table = 'TEMPERATURE'

# On python anywhere I had to create the table manually, with the following command:
# CREATE TABLE TEMPERATURE (id int NOT NULL AUTO_INCREMENT, TEMPERATURE decimal(5,2), REGISTERED_AT datetime, primary key (id));
# Later I had to add two new columns, TEMPERATURE_OBSERVATORY and TIME_OBSERVATORY, with the following commands
# ALTER TABLE TEMPERATURE ADD COLUMN TEMPERATURE_OBSERVATORY decimal(5,2);
# ALTER TABLE TEMPERATURE ADD COLUMN TIME_OBSERVATORY DATETIME;
# Logged on the right database