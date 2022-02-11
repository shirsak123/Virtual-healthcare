from django.db import models

# Create your models here.

class ReviewRating(models.Model):
    review_doctor = models.ForeignKey('accounts.Doctor',on_delete=models.CASCADE)
    review_patient = models.ForeignKey('accounts.Patient',on_delete=models.CASCADE)
    subject = models.CharField(max_length=100,blank= True)
    review = models.TextField(max_length=500,blank= True)
    rating = models.IntegerField()
    review_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject