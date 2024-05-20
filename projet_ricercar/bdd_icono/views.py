from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from bdd_icono.models import Image
from django.views import generic

def home(request):
    from bdd_icono.forms import FormulaireRecherche
    from django.db.models import Q
    if request.method == "POST":
        form = FormulaireRecherche(request.POST)
        if form.is_valid():
            res_image = Image.objects.all()
            param=request.POST.get('image')
            res_image.filter(
                Q(n_cesr__icontains=param)
            ).distinct
            paginator = Paginator(res_image, 10)

            page = request.GET.get('page')
            images = paginator.get_page(page)
            context = {
                'images' : images
            }
            return HttpResponseRedirect("/resultats", context)
    else:
        form = FormulaireRecherche()
    return render(request, 'bdd_icono/home.html', {'formulaire':form})

def inProgress(request):
    return render(request, 'bdd_icono/in_progress.html')


def recherche(request):
    return render(request, 'bdd_icono/recherche.html')

def resultats(request):
    from django.db.models import Q
    query = request.GET.get('query')
    images = Image.objects.all()
    if query:
        images.filter(
            Q(n_cesr__icontains=query)| \
            Q(description__icontains=query)| \
            Q(commentaire__icontains=query)
        ).distinct
    context = {
        'image' : images
    }
    paginator = Paginator(images, 5)

    page = request.GET.get('page')
    images = paginator.get_page(page)
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
