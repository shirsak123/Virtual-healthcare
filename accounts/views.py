from django.shortcuts import render,redirect, get_object_or_404
from .forms import PatientSignupForm, DoctorSignupForm, UserForm,PatientProfileForm,DoctorProfileForm
from .models import User,Patient,Doctor,PatientProfile,DoctorProfile
from specialist.models import Specialist
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from appointment.forms import Appointment 
from appointment.models import Appointment as app

#Custom decorators
from .decorator import unauthenticated_user

#Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.


#------------------------------------------------Register View------------------------------------------------

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            blood = form.cleaned_data['blood']
            password = form.cleaned_data['password1']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']


            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                password=password,
                dob=dob,
                gender=gender

            )
            patient = Patient.objects.create(user=user,blood=blood)
            prof = PatientProfile.objects.create(user=user)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please Active Your Account'
            message = render_to_string('accounts/patient/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message,to=[to_email])
            send_email.send()
            messages.success(request,'One more step. Please verify its you in your email.')
            return redirect('/accounts/login/?command=verification&email='+email)
        else:
            messages.error(request,"Some error occured")
    else:
        form = PatientSignupForm()

    return render(request, 'accounts/patient/register.html',{'form':form})

@unauthenticated_user
def registerDoctor(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            location = form.cleaned_data['location']
            specialist = form.cleaned_data['specialist']
            password = form.cleaned_data['password1']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']


            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password,
                is_doctor=True,
                is_patient=False,
                dob=dob,
                gender=gender

            )
            doctor = Doctor.objects.create(user=user,specialist=specialist,location=location)
            doc_profile = DoctorProfile.objects.create(user=user)
            user.save()

            messages.success(request,'You have been registered but wait for your account approval')
            return redirect('login')
        else:
            messages.error(request,"Something went wrong")
    else:
        form = DoctorSignupForm()
    specialist = Specialist.objects.all()
    return render(request, 'accounts/doctor/register.html',{'form':form,'specialist':specialist})

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are logged in succesfully')
            return redirect('homeAfter')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('login')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset Password
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message,to=[to_email])
            send_email.send()

            messages.success(request,'Password reset email sent succesfully')
            return redirect('login')

        else:
            messages.error(request,"Account does not exist")
            return redirect('forgotPassword')
    return render(request,'accounts/forgot.html')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Your account has been activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']  = uid
        messages.success(request,"Please reset your password")
        return redirect('resetPassword')
    else:
        messages.error(request,'This is a invalid link. Please try again')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request,"Password do not match")
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')

@login_required(login_url = 'login')
def changePassword(request):
    if request.method == 'POST':
        current_password = request.POST['currentPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['newPassword2']

        user = User.objects.get(email__exact=request.user.email)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,"The Password was changed successfully. Please Login")
                return redirect('login')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('changePassword')
        else:
            messages.error(request,'Password does not match')
            return redirect('changePassword')
    else:
        return render(request,'accounts/changePassword.html')

@login_required(login_url = "login")
def dashboard(request):
    if request.user.is_patient:
        apps = app.objects.filter(patient_app = request.user.patient).count()
        confirm_count = app.objects.filter(patient_app = request.user.patient,status="confirm").count()
        context = {'app':apps,'confirm_one':confirm_count}
        return render(request,'accounts/patient/dashboard.html',context)
    else:
        apps = app.objects.filter(doctor_app=request.user.doctor)
        count = {}
        can = app.objects.filter(status="cancelled",doctor_app=request.user.doctor).count()
        con = app.objects.filter(status="confirm",doctor_app=request.user.doctor).count()
        pen = app.objects.filter(status="pending",doctor_app=request.user.doctor).count()
        count['pendingCount'] = pen
        count['canCon'] = can + con
        context = {
            'apps':apps,
            'count':count
        }
        return render(request,'accounts/doctor/Doctordashboard.html',context)

@login_required(login_url = 'login')
def editProfile(request):
    if request.user.is_patient:
        patprofile = get_object_or_404(PatientProfile,user=request.user)
        if request.method == 'POST':
            user_form = UserForm(request.POST,instance=request.user)
            patient_form = PatientProfileForm(request.POST,request.FILES,instance=patprofile)
            if user_form.is_valid() and patient_form.is_valid():
                user_form.save()
                patient_form.save()
                messages.success(request,"Your profile has been updated")
                return redirect('editProfile')
        else:
            user_form = UserForm(instance=request.user)
            patient_form = PatientProfileForm(instance=patprofile)
        context = {
            'user_form':user_form,
            'patient_form':patient_form,
        }
        return render(request,'accounts/patient/editProfile.html',context)
    else:
        docprofile = get_object_or_404(DoctorProfile,user=request.user)
        if request.method == 'POST':
            user_form = UserForm(request.POST,instance=request.user)
            doctor_form = DoctorProfileForm(request.POST,request.FILES,instance=docprofile)
            print(user_form.is_valid(),doctor_form.is_valid())
            if user_form.is_valid() and doctor_form.is_valid():
                user_form.save()
                doctor_form.save()
                messages.success(request,"Your profile has been updated")
                return redirect('editProfile')
        else:
            user_form = UserForm(instance=request.user)
            doctor_form = DoctorProfileForm(instance=docprofile)

        context = {
            'user_form':user_form,
            'doctor_form':doctor_form,
        }
        return render(request,'accounts/doctor/editProfile.html',context)

@login_required(login_url = 'login')
def myAppointment(request):
    userprofile = PatientProfile.objects.get(user_id=request.user.id)
    user_appointment = app.objects.filter(patient_app_id=request.user.id)    
    context ={
        'userprofile': userprofile,
        'appoint':user_appointment,
        }
    return render(request,'accounts/patient/myAppointment.html',context)

@login_required(login_url = 'login')
def doctorAppointment(request):
    docprofile = DoctorProfile.objects.get(user_id=request.user.id)
    doc_appointment = app.objects.filter(doctor_app_id=request.user.id)    
    context ={
        'docprofile': docprofile,
        'doc_appointment':doc_appointment,
        }
    return render(request,'accounts/doctor/myAppointment.html',context)

@login_required(login_url='login')
def myPatients(request):
    apps = app.objects.filter(doctor_app=request.user.doctor)
    context = {
        'app':apps
    }
    return render(request,'accounts/doctor/myPatients.html',context)
