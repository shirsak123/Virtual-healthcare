from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.homeAfter, name='homeAfter'),
    path('search/',views.search, name='search'),
    path('specialist/<slug:specialist_slug>/',views.specialistCat,name='BySpecialist'),
    path('specialist/<slug:specialist_slug>/<slug:doctor_slug>',views.doctorDetail,name='doctorDetail'),
    path('specialist/<slug:specialist_slug>/<slug:doctor_slug>/bookAppointment',views.doctorAppointment,name='doctorAppointment'),
    path('specialist/<slug:specialist_slug>/<slug:doctor_slug>/appointmentDetails/<int:appko_id>',views.appointmentDetails,name='appointmentDetails'),
    path('patient/<slug:patient_slug>/<int:appk_id>', views.appDetailPatient,name="appDetailPatient"),
    path('submitReview/<int:doctor_id>', views.submitReview,name="submitReview"),
]