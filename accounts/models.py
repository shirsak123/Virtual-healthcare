from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from specialist.models import Specialist
from appointment.models import Appointment
from django.utils.text import slugify
from datetime import datetime,date
from search.models import ReviewRating
from django.db.models.aggregates import Avg
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('gender',1)


        if extra_fields.get('is_staff') is not True:
            raise ValueError("Staff must be true")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be true")
        return self.create_user(email,password,**extra_fields)

class User(AbstractUser):
    GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)

    username = None
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=40,unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    dob = models.DateField(auto_now_add=False,null=True,blank=False)
    gender = models.IntegerField(choices=GENDER_CHOICES,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
  

class Patient(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    slug = models.SlugField(max_length=50,unique=True)
    blood = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.first_name+"-"+self.user.last_name)+"-"+str(self.user.id)
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name


class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    slug = models.SlugField(max_length=50,unique=True)
    specialist = models.ForeignKey(Specialist,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.first_name+"-"+self.user.last_name)+"-"+str(self.user.id)
        super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(review_doctor=self,review_status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = int(reviews['average'])
        return avg

    def age(self):
        return int((datetime.now().date() - self.user.dob).days / 365.25)
        

    def totalRating(self):
        reviews = ReviewRating.objects.filter(review_doctor=self,review_status=True).count()
        return reviews

    def avgLike(self):
        likes = ReviewRating.objects.filter(review_doctor=self,review_status=True,rating__gte=3).count()
        total = ReviewRating.objects.filter(review_doctor=self,review_status=True).count()
        try:
            z = int((likes/total)*100)
        except ZeroDivisionError:
            z = 0

        return z

class PatientProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address_1 =  models.CharField(max_length=100,blank=True)
    address_2 =  models.CharField(max_length=100,blank=True)
    profile_pic = models.ImageField(blank=True, upload_to='profile/patient',default='profile/default_user.jpg')

    def __str__(self):
        return self.user.first_name

class DoctorProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    about_me = models.TextField(max_length=2000,blank=False)
    address_1 =  models.CharField(max_length=100,blank=True)
    address_2 =  models.CharField(max_length=100,blank=True)
    profile_pic = models.ImageField(blank=True,upload_to='profile/doctor',default='profile/default_user.jpg')

    education1 = models.CharField(max_length=50,blank=True,null=True)
    university1 = models.CharField(max_length=50,blank=True,null=True)
    from_year1 = models.CharField(max_length=50,blank=True,null=True)
    to_year1 = models.CharField(max_length=50,blank=True,null=True)

    education2 = models.CharField(max_length=50,blank=True,null=True)
    university2 = models.CharField(max_length=50,blank=True,null=True)
    from_year2 = models.CharField(max_length=50,blank=True,null=True)
    to_year2 = models.CharField(max_length=50,blank=True,null=True)

    professtion_title1 = models.CharField(max_length=50,blank=True,null=True)
    professtion_from_year1 = models.CharField(max_length=50,blank=True,null=True)
    professtion_to_year1 = models.CharField(max_length=50,blank=True,null=True)
    place_1 = models.CharField(max_length=50,blank=True,null=True)
    
    place_2 = models.CharField(max_length=50,blank=True,null=True)
    professtion_title2 = models.CharField(max_length=50,blank=True,null=True)
    professtion_from_year2 = models.CharField(max_length=50,blank=True,null=True)
    professtion_to_year2 = models.CharField(max_length=50,blank=True,null=True)

    services = models.CharField(max_length=200,blank=True,null=False)
    specialization = models.CharField(max_length=200,blank=True,null=False)


    
    def __str__(self):
        return self.user.first_name