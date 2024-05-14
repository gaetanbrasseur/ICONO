from django.shortcuts import render
from django.http import HttpResponse
from bdd_icono.models import Image
from django.views import generic

def home(request):
    img_count = Image.objects.count()
    context = {
        'nombre_image' : img_count
    }
    return render(request, 'bdd_icono/home.html',context)