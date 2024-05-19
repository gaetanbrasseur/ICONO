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

def inProgress(request):
    return render(request, 'bdd_icono/in_progress.html')


def recherche(request):
    return render(request, 'bdd_icono/recherche.html')

def resultats(request):
    images = Image.objects.all
    
    context = {
        'images' : images
    }
    return render(request, 'bdd_icono/resultats.html',context)

def image(request, id_image):
    from django.http import Http404

    try :
        image = Image.objects.get(id=id_image)
    except Image.DoesNotExist:
        raise Http404("Aucun auteur trouvé pour cet identifiant")
    context = {
        'image' : image
    }

    return render(request, 'bdd_icono/image.html', context)
