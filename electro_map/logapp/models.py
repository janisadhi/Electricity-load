from django.db import models

# Create your models here.
from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    predicted_consumption = models.FloatField()
    allocated_power = models.FloatField()
    surplus_deficit = models.FloatField()

    def __str__(self):
        return self.name

