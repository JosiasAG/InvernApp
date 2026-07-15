from django.utils import timezone

from django.shortcuts import render
from .models import Cultivo, LoteCultivo, TareaProgramada, Invernadero, Zona, Cama, Insumo, UsoInsumo, Proveedor, CatalogoInsumos


def home(request):
    return render(request, 'base.html')

def lista_tareas(request):
    if request.method == 'GET':
        fecha_hoy = timezone.localdate()
        tareas = TareaProgramada.objects.filter(fecha_programada=fecha_hoy).order_by('fecha_programada')
        return render(request, 'lista_tareas.html', {
            'tareas': tareas,
            'hoy': fecha_hoy
        })
    elif request.method == 'POST':
        fecha_filtro = request.POST.get('fecha_filtro')
        tareas = TareaProgramada.objects.filter(fecha_programada=fecha_filtro).order_by('fecha_programada')
        fecha_hoy = timezone.datetime.strptime(fecha_filtro, "%Y-%m-%d").strftime("%d/%m/%Y")
        return render(request, 'lista_tareas.html', {
        'tareas': tareas,
        'hoy': fecha_hoy
        })