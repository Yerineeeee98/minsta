from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "posts"

urlpatterns = [
    path('', views.index, name = "index"),
    path('create/', views.create, name = "create"),
    
]

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)