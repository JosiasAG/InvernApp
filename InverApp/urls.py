from django.contrib import admin
from django.urls import path
from cultivos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('lista_tareas/', views.lista_tareas, name='lista_tareas'),
]
