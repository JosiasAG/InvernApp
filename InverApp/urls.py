from django.contrib import admin
from django.urls import path
from cultivos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('lista_tareas/', views.lista_tareas, name='lista_tareas'),
    path('detalle_tarea/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('registrar_planta/', views.registrar_planta, name = 'registrar_planta'),
    path('registrar_invernadero/', views.registrar_invernadero, name='registrar_invernadero'),
    path('registrar_bloque/', views.registrar_bloque, name="registrar_bloque"),
    path('ver_plantas/', views.ver_plantas, name="ver_plantas"),
]
