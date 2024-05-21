from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from bdd_icono.models import Image
from django.views import generic

def home(request):
    from bdd_icono.forms import FormulaireRecherche
    form = FormulaireRecherche()
    return render(request, 'bdd_icono/home.html', {'formulaire':form})

def inProgress(request):
    return render(request, 'bdd_icono/in_progress.html')


def recherche(request):
    return render(request, 'bdd_icono/recherche.html')

def resultats(request):
    from django.db.models import Q 
    images = Image.objects.all()
    param_image = request.POST.get('image')
    images = images.filter(
        Q(commentaire__icontains=param_image)
    )
    context = {
        'images' : images,
        'param' : param_image
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
