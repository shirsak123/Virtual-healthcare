from django.urls import path
from . import views

urlpatterns = [
    path("",views.adminHome,name="adminHome"),
    path("login/",views.adminLogin,name="adminLogin"),
    path("patients/",views.adminPatient,name="adminPatient"),
    path("specialists/",views.adminSpecialists,name="adminSpecialists"),
    path("doctors/",views.adminDoctors,name="adminDoctors"),
    path("reviews/",views.adminReviews,name="adminReviews"),
    path("appointments/",views.adminAppointments,name="adminAppointments"),
    path("admins/",views.adminAdmins,name="adminAdmins"),
    path("pharmacies/",views.adminPharmacies,name="adminPharmacies"),

]