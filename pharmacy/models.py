from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.

class Pharmacy(models.Model):
    pharmacy_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    opens_at = models.CharField(max_length=100)
    closes_at = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5),])
    photo = models.ImageField(blank=True,upload_to='pharmacy/',default='profile/default_pharmacy.jpg')

    class Meta:
        verbose_name_plural = "Pharmacies"
    
    def __str__(self):
        return self.pharmacy_name