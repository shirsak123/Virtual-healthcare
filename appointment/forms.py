from django import forms
from .models import Appointment
import datetime as dt

class DateInput(forms.DateInput):
    input_type = 'date'

HOUR_CHOICES = [(dt.time(hour=x),'{:02d}:00'.format(x)) for x in range(0, 24)]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['app_time','app_date','note_title','note_body','reply_note']
        widgets = {'app_time': forms.Select(choices=HOUR_CHOICES),
            'app_date':DateInput()}

    def clean_date(self):
            date = self.cleaned_data['app_date']
            if date < dt.date.today():
                print(date,dt.date.today())
                raise forms.ValidationError()
            

    def __init__(self,*args,**kwargs):
        super(AppointmentForm, self).__init__(*args,**kwargs)
        self.fields['note_body'].widget.attrs['placeholder']='Your Problem Description'
        self.fields['note_title'].widget.attrs['placeholder']='Your Problem Title'
        self.fields['reply_note'].widget.attrs['placeholder']='Reply Note For the Patient'
        self.fields['reply_note'].widget.attrs['required'] ='True'


        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control floating my-1'

    