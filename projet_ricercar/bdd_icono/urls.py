from django.urls import path
from bdd_icono import views
from django.conf import settings
from django.conf.urls.static import static
# Create your views here.
urlpatterns =[
    path('',views.home, name="home"),
    path('inprogress/', views.inProgress, name='in_progress'),
    path('recherche/', views.recherche, name='recherche'),
    path('resultats/', views.resultats, name='resultats'),
    path('image/<int:id_image>/', views.image, name='image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)