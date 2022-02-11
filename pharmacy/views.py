from django.shortcuts import render
from .models import Pharmacy

# Create your views here.

def pharmacySearch(request):
    pharmacy = Pharmacy.objects.all()
    context = {
        'pharmacy':pharmacy
    }
    return render(request,'pharmacy/pharmacy_search.html',context)

