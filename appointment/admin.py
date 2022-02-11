from django.contrib import admin
from .models import Appointment

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    ordering=('created_at',)
    list_display = ('getID','app_time','app_date','created_at','updated_at')
    


admin.site.register(Appointment,AppointmentAdmin)
