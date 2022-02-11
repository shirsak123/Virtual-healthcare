from django.db import models

# Create your models here.
class Specialist(models.Model):
    specialist_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50,unique=True)

    def __str__(self):
        return self.specialist_name