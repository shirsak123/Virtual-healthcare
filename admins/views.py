from django.shortcuts import redirect, render
from accounts.models import Doctor, Patient, User
from appointment.models import Appointment
from search.models import ReviewRating
from .decorators import unauthenticated_user,is_user_admin
from django.contrib import messages,auth
from specialist.models import Specialist
from pharmacy.models import Pharmacy

# Create your views here.

@unauthenticated_user
def adminLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are logged in succesfully')
            return redirect('adminHome')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('adminLogin')
        
    return render(request, 'admindashboard/login.html')

@is_user_admin
def adminHome(request):
    print(request.path)
    patient = Patient.objects.all().count()
    doctor = Doctor.objects.all().count()
    appointment = Appointment.objects.all().count()
    review = ReviewRating.objects.all().count()

    patient_list = Patient.objects.order_by('user__created_at')[:5]
    doctor_list = Doctor.objects.order_by('user__created_at')[:5]
    appointment_list = Appointment.objects.order_by('created_at')[:5]


    context = {
        'patient_count':patient,
        'doctor_count':doctor,
        'appointment_count':appointment,
        'review_count':review,
        'patient_list':patient_list,
        'doctor_list':doctor_list,
        'appointment_list':appointment_list
    }
    
    return render(request,'admindashboard/dashboard.html',context)

@is_user_admin
def adminPatient(request):
    patient = Patient.objects.all()
    context = {
        'patient_list':patient
    }

    return render(request,'admindashboard/patient.html',context)

@is_user_admin
def adminSpecialists(request):
    specialist = Specialist.objects.all()
    context = {
        'specialist_list':specialist
    }

    return render(request,'admindashboard/specialist.html',context)

@is_user_admin
def adminDoctors(request):
    doctor = Doctor.objects.all()

    context = {
        'doctor_list':doctor
    }

    return render(request,'admindashboard/doctor.html',context)

@is_user_admin
def adminReviews(request):
    reviews = ReviewRating.objects.all()

    context = {
        'review_list':reviews
    }

    return render(request,'admindashboard/reviews.html',context)

@is_user_admin
def adminAppointments(request):
    appointment = Appointment.objects.all()

    context = {
        'appointment_list':appointment
    }

    return render(request,'admindashboard/appointment.html',context)

@is_user_admin
def adminAdmins(request):
    admins = User.objects.filter(is_superuser = True)
    context = {
        'admin_list':admins
    }

    return render(request,'admindashboard/admin.html',context)
    
@is_user_admin
def adminPharmacies(request):
    pharmacy = Pharmacy.objects.all()
    context = {
        'pharmacy_list':pharmacy
    }

    return render(request,'admindashboard/pharmacy.html',context)
