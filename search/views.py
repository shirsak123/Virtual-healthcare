from django.shortcuts import get_object_or_404, redirect, render
from specialist.models import Specialist
from django.http import HttpResponse
from accounts.models import Doctor, DoctorProfile, Patient, PatientProfile
from appointment.forms import AppointmentForm
from appointment.models import Appointment
from django.contrib import messages
from search.forms import ReviewForm

from accounts.decorator import is_user_patient

from django.contrib.auth.decorators import login_required
from search.models import ReviewRating
from django.db.models import Q

# Sorting Methods
def getavg(obj):
    return obj.averageReview()
def gettotal(obj):
    return obj.totalRating()
def getavglike(obj):
    return obj.avgLike()
# end

def home(request):
    return render(request,'home.html')

@login_required(login_url = 'login')
def homeAfter(request):
    specialist = Specialist.objects.all()[:6]
    qs = Doctor.objects.filter()
    a = sorted(qs,key=getavg,reverse=True)[:6]
    context = {
        'specialist':specialist,
        'sorted_doc':a,
    }
    if request.user.is_patient:
        app = Appointment.objects.filter(patient_app=request.user.patient)
        for i in a:
            for j in app:
                if i.slug == j.doctor_app.slug:
                    i.appointed=True and j.status == "pending"
                    i.pp = j.id
   
        context['app'] = app
    return render(request,'home-search/home-after.html',context)

@login_required(login_url = 'login')
@is_user_patient
def search(request):
    GENDER_CHOICES = {
        'male':0,
        'female':1,
        'not specified':2}
    if 'specialist_name' in request.GET:
        keyword = request.GET['specialist_name']
        if keyword:
            doctor = Doctor.objects.filter(specialist__specialist_name__contains=keyword)
        else:
            doctor = Doctor.objects.filter()
    elif 'select_specialist' in request.GET and 'gender_type' in request.GET:
        search_filter = request.GET.getlist('select_specialist')
        gender_type = request.GET.getlist('gender_type')
        
        for i in range(len(gender_type)):
            gender_type[i] = GENDER_CHOICES[gender_type[i]]
        doctor = Doctor.objects.filter(specialist__specialist_name__in=search_filter,user__gender__in=gender_type)
    elif 'select_specialist' in request.GET or 'gender_type' in request.GET:
        search_filter = request.GET.getlist('select_specialist')
        gender_type = request.GET.getlist('gender_type')
        for i in range(len(gender_type)):
            gender_type[i] = GENDER_CHOICES[gender_type[i]]
        doctor = Doctor.objects.filter(Q(specialist__specialist_name__in=search_filter) | Q(user__gender__in=gender_type))
    else:
        doctor = Doctor.objects.all()

    if 'sort_by' in request.GET and request.GET['sort_by'] != "Select":
        get_name = globals()[request.GET['sort_by']]
        doctor = sorted(doctor,key=get_name,reverse=True)
    app = Appointment.objects.filter(patient_app=request.user.patient)
    for i in doctor:
        for j in app:
            if i.slug == j.doctor_app.slug:
                i.appointed=True and j.status == "pending"
                i.pp = j.id
    context = {
        'doctors':doctor,
        'app':app
    }
    return render(request,'home-search/search.html',context)

@login_required(login_url = 'login')
@is_user_patient
def specialistCat(request,specialist_slug=None):
    specialist = get_object_or_404(Specialist, slug=specialist_slug)
    doctor = Doctor.objects.filter(specialist__specialist_name__contains=specialist)
    
    context = {
        'doctors':doctor
    }
    return render(request,'home-search/search.html',context)

@login_required(login_url = 'login')
@is_user_patient
def doctorDetail(request,specialist_slug,doctor_slug):
    try:
        doc_details = Doctor.objects.get(specialist__slug=specialist_slug,slug = doctor_slug)
        doc_profile = DoctorProfile.objects.get(user=doc_details.user)
        app = Appointment.objects.filter(doctor_app=doc_details.user.doctor)
        if app.exists():
            app = app[0]
    except Exception as e:
        raise e

    try:
        doc_details = Doctor.objects.get(specialist__slug=specialist_slug,slug = doctor_slug)
        isBooked = Appointment.objects.filter(doctor_app = doc_details.user.doctor,patient_app = request.user.patient,status='confirm').exists()
    except Appointment.DoesNotExist:
        isBooked = None

    reviews = ReviewRating.objects.filter(review_doctor__slug=doctor_slug,review_status= True).order_by('-created_at')
    services = doc_profile.services.split(';')
    specialization = doc_profile.specialization.split(';')
    context = {
        'docs':doc_details,
        'doc_profile':doc_profile,
        'app':app,
        'isbooked':isBooked,
        'reviews':reviews,
        'services':services,
        'specializations':specialization
    }
    return render(request,'accounts/doctor/doctor-details.html',context)

@login_required(login_url = 'login')
@is_user_patient
def doctorAppointment(request,specialist_slug,doctor_slug):
    try:
        doc_details = Doctor.objects.get(specialist__slug=specialist_slug,slug = doctor_slug)
        doc_profile = DoctorProfile.objects.get(user=doc_details.user)
        if request.method == 'POST':
            appointment = AppointmentForm(request.POST)
            if appointment.is_valid():
                app = appointment.save(commit=False)
                app.patient_app = request.user.patient
                app.doctor_app = doc_details
                app.save()
                messages.success(request,"Appointment has been sent")
                return redirect('dashboard')  
            else:
                messages.error(request,"Apppointment date cannot be in past!")

        else:
            appointment = AppointmentForm()          
    except Exception as e:
        raise e
    context = {
        'docs':doc_details,
        'doc_profile':doc_profile,
        'appointment':appointment
    }
    return render(request,'appointments/appointment.html',context)

@login_required(login_url = 'login')
def appointmentDetails(request,specialist_slug,doctor_slug,appko_id):
    doc_details = Doctor.objects.get(specialist__slug=specialist_slug,slug = doctor_slug)
    doc_profile = DoctorProfile.objects.get(user=doc_details.user)
    app = Appointment.objects.get(doctor_app=doc_details.user.doctor,patient_app_id=request.user.id, id=appko_id)
    context = {
        'docs':doc_details,
        'doc_profile':doc_profile,
        'app':app
    }
    return render(request,'appointments/appointment_details.html',context)


@login_required(login_url = 'login')
def appDetailPatient(request,patient_slug,appk_id):
    try:
        pat_details = Patient.objects.get(slug = patient_slug)
        pat_profile = PatientProfile.objects.get(user=pat_details.user)
        appointment = Appointment.objects.get(doctor_app=request.user.doctor,patient_app=pat_details.user.patient,id=appk_id)      
        if request.method == 'POST':
            appointment_form = AppointmentForm(request.POST,instance=appointment)
            if appointment_form.is_valid():
                app = appointment_form.save(commit=False)
                app.patient_app = pat_details
                app.doctor_app = request.user.doctor
                if 'decline' in request.POST:
                    app.status= 'cancelled'
                else:
                    app.status = 'confirm'
                app.save()
            return redirect('homeAfter') 
        else:
            appointment_form = AppointmentForm(instance=appointment)
    except Exception as e:
        raise e
    context = {
        'pats':pat_details,
        'pat_profile':pat_profile,
        'app':appointment_form,
        'apps': appointment
    }
    return render(request,'appointments/doctor_app.html',context)


@login_required(login_url = 'login')
def submitReview(request, doctor_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(review_patient=request.user.patient, review_doctor_id=doctor_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! Your review has been updated')
            return redirect(url+"#doc_reviews")
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.review_patient_id = request.user.id
                data.review_doctor_id = doctor_id
                data.save()
                messages.success(request,'Thank you! Your review has been submitted')
                return redirect(url+"#doc_reviews")



