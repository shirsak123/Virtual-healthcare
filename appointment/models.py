from django.db import models
import datetime as dt

# Create your models here.

class Appointment(models.Model):
    patient_app = models.ForeignKey('accounts.Patient',on_delete=models.PROTECT)
    doctor_app = models.ForeignKey('accounts.Doctor',on_delete=models.PROTECT)
    app_date = models.DateField(auto_now_add=False,null=True,blank=False)
    app_time = models.TimeField(default=dt.time(00,00))
    note_title = models.CharField(max_length=100,blank=False)
    note_body = models.TextField(max_length=1000,blank=False)
    reply_note = models.TextField(max_length=1000,null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,default="pending")
    

    def getID(self):
        return self.id
        