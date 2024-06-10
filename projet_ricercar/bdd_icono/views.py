from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from bdd_icono.models import Image
from django.views import generic
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth import logout
import os

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
        Q(description__icontains=param_image) | Q(legende__icontains=param_image) | Q(cote__icontains=param_image)
        | Q(mots_cles__mot_cle_libelle__icontains=param_image) | Q(themes__theme_libelle__icontains=param_image)
        | Q(fk_extrait_de__extrait_de_nom__icontains=param_image)
    ).distinct()
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
    liste_types = list(image.mots_cles.values_list('mot_cle_type', flat=True).distinct())
    ordered_mots_cles = dict()
    for type in liste_types:
        ordered_mots_cles[type.capitalize()] =  image.mots_cles.filter(mot_cle_type=type)
    context = {
        'image' : image,
        'ordered_mots_cles' : ordered_mots_cles 
    }

    return render(request, 'bdd_icono/image.html', context)

@login_required
def download_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    file_path = image.lien_telechargement.path

    if not os.path.exists(file_path):
        raise Http404("Le fichier spécifié est introuvable.")
    
    try:
        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    except Exception as e:
        raise Http404(f"Erreur lors de la tentative de téléchargement : {e}")


def deconnexion(request):
    logout(request)
    return redirect('home')

class CustomLoginView(auth_views.LoginView):
    template_name = 'bdd_icono/login.html'

class CustomLogoutView(auth_views.LogoutView):
    template_name = 'bdd_icono/logout.html'
