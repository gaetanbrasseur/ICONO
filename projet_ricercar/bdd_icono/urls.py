from django.urls import path
from bdd_icono import views
from django.conf import settings
from django.conf.urls.static import static
# Create your views here.
urlpatterns =[
    path('',views.home, name="home"),
    path('inprogress/', views.inProgress, name='in_progress')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)