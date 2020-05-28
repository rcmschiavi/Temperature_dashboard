from django.db import models

# Create your models here.
class Agriculture_data(models.Model):
    TEMPERATURE = models.DecimalField(max_digits=5,decimal_places=2)
    HUMIDITY = models.DecimalField(max_digits=5,decimal_places=2)
    MOISTURE = models.DecimalField(max_digits=5,decimal_places=2)
    REGISTERED_AT = models.DateTimeField(auto_now=True)
    class Meta:
       managed = True
       db_table = 'AGRICULTURE'


# On python anywhere I had to create the table manually, with the following command:
# CREATE TABLE AGRICULTURE (id int NOT NULL AUTO_INCREMENT, TEMPERATURE decimal(5,2), HUMIDITY decimal(5,2), MOISTURE decimal(5,2), REGISTERED_AT datetime, primary key (id));