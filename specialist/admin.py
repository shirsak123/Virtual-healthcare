from django.contrib import admin
from .models import Specialist

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('specialist_name',)}
    list_display = ('specialist_name','slug')

admin.site.register(Specialist, CategoryAdmin)