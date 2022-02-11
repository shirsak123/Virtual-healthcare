from django.contrib import admin
from .models import User,Patient,Doctor
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, PatientProfile, DoctorProfile


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name','is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active','is_doctor','is_patient')
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name','dob','address','gender','phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_doctor','is_patient',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name','is_staff', 'is_active','is_doctor','is_patient',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



class PatientProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style"border-radius:50%;">'.format(object.profile_pic.url))
    thumbnail.short_description = "Profile Picture"
    list_display = ('thumbnail','user','address_1','address_2')

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(DoctorProfile)
