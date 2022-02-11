from django.urls import path
from . import views

urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("forgotPassword/",views.forgotPassword, name="forgotPassword"),
    path("resetPassword/",views.resetPassword, name="resetPassword"),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name="resetpassword_validate"),
    path('changePassword/', views.changePassword, name="changePassword"),


    #------------Conditional--------------------------
    path("logout/",views.logout,name="logout"),
    path("login/",views.login,name="login"),
    path("editProfile/",views.editProfile,name="editProfile"),

    #--------Patient URLS-----------
    path("register/",views.register,name="register"),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("myAppointment/",views.myAppointment,name="myAppointment"),


    #--------------Doctor URLS-----------------------------
    path("doctor/register/",views.registerDoctor,name="registerDoctor"),
    path("doctor/appointment/",views.doctorAppointment,name="doctorAppointment"),
    path("doctor/mypatients/",views.myPatients,name="myPatients"),
]