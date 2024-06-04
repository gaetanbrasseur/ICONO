from django.urls import path
from bdd_icono import views
from django.conf import settings
from django.conf.urls.static import static
from .views import download_image, CustomLoginView, CustomLogoutView


urlpatterns =[
    path('',views.home, name="home"),
    path('inprogress/', views.inProgress, name='in_progress'),
    path('resultats/', views.resultats, name='resultats'),
    path('image/<int:id_image>/', views.image, name='image'),
    path('download/<int:image_id>/', download_image, name='download_image'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.deconnexion, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
