from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient,Doctor,User,PatientProfile,DoctorProfile
from django import forms
from specialist.models import Specialist


class DateInput(forms.DateInput):
    input_type = 'date'

class PatientSignupForm(UserCreationForm):
    BLOOD_TYPE= [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O-','O-'),
    ('O+', 'O+')
    ]
    blood = forms.CharField(max_length=100, widget=forms.Select(choices=BLOOD_TYPE))

    class Meta:
        model = User
        widgets = {'dob':DateInput()}
        fields = ['email','first_name','last_name','password1','password2','phone_number',
        'address','dob','gender']


    def __init__(self,*args,**kwargs):
        super(PatientSignupForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

class DoctorSignupForm(UserCreationForm):
    location = [
        ('Kathmandu','Kathmandu')
    ]
    specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
    location = forms.CharField(max_length=100,widget=forms.Select(choices=location))



    class Meta:
        model = User
        widgets = {'dob':DateInput()}
        fields = ['email','first_name','last_name','password1','password2','phone_number',
        'specialist','dob','gender']


    def __init__(self,*args,**kwargs):
        super(DoctorSignupForm, self).__init__(*args,**kwargs)
        # self.fields['first_name'].widget.attrs['placeholder']='Enter Your First Name'
        # self.fields['last_name'].widget.attrs['placeholder']='Enter Your Last Name'
        # self.fields['email'].widget.attrs['placeholder']='Enter Your Email'
        # self.fields['password1'].widget.attrs['placeholder']='Password'
        # self.fields['password2'].widget.attrs['placeholder']='Repeat Password'
        # self.fields['location'].widget.attrs['placeholder']='Enter Your Location'
        # self.fields['phone_number'].widget.attrs['placeholder']='Enter Your Phone Number'
        # self.fields['blood'].widget.attrs['placeholder']='Enter Your Blood Group'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control floating'




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number',
        'address']
    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control floating'


class PatientProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, error_messages= {'invalid':{'Image files only'}}, widget=forms.FileInput)
    class Meta:
        model = PatientProfile
        fields = ('address_1', 'address_2','profile_pic')
    def __init__(self,*args,**kwargs):
        super(PatientProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control floating'

class DoctorProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, error_messages= {'invalid':{'Image files only'}}, widget=forms.FileInput)
    class Meta:
        model = DoctorProfile
        fields = ('address_1', 'address_2','about_me','profile_pic',
        'education1','university1','from_year1','to_year1',
        'education2','university2','from_year2','to_year2',
        'professtion_title1','place_1','professtion_from_year1','professtion_to_year1',
        'professtion_title2','place_2','professtion_from_year2','professtion_to_year2',
        'services','specialization'
        )
    def __init__(self,*args,**kwargs):
        super(DoctorProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control floating'

#     @transaction.atomic
#     def data_save(self):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#         patient = Patient.objects.create(user=user)
#         patient.blood = self.cleaned_data.get('blood')
#         patient.save()
#         return user

# class DoctorSignupForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     specialist = forms.CharField(required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User

