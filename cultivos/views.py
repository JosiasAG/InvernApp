from django.utils import timezone

from django.shortcuts import render
from .models import Cultivo, LoteCultivo, TareaProgramada, Invernadero, Bloque, Cama, Insumo, UsoInsumo, Proveedor, CatalogoInsumos
from .forms import formulario_nuevo_lote, formulario_cultivo, formulario_invernadero

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
    
def detalle_tarea(request, tarea_id):
    tarea = TareaProgramada.objects.get(id=tarea_id)

    if tarea.tipo_tarea == 'RIEGO':
        return render(request, 'detalle_tarea.html', {
        'riego': tarea
    })
    elif tarea.tipo_tarea == 'PODA':
        return render(request, 'detalle_tarea.html', {
        'poda': tarea
    })
    elif tarea.tipo_tarea == 'FERTILIZACION':
        return render(request, 'detalle_tarea.html', {
        'fertilizacion': tarea
    })
    elif tarea.tipo_tarea == 'FUMIGACION':
        return render(request, 'detalle_tarea.html', {
        'fumigacion': tarea
    })
    else: 
        return render(request, 'detalle_tarea.html', {
        'cosecha': tarea
    })

def crear_tarea(request):
    if request.method == "GET":
        return render (request, "crear_lote.html", {
            'form': formulario_nuevo_lote}) 
    elif request.method=="POST":
        form = formulario_nuevo_lote(request.POST)
        nueva_tarea = form.save(commit=False)
        nueva_tarea.save()
        return render (request, "crear_lote.html", {
            'form': formulario_nuevo_lote}) 
    
def registrar_planta(request):
    if request.method=="GET":     
        return render (request, 'registrar_planta.html', {
            'form' : formulario_cultivo
        })
    elif request.method=="POST":
        return render (request, 'registrar_planta.html', {
            'form' : formulario_cultivo
        })

def registrar_invernadero(request):
    if request.method=="GET":    
        return render (request, 'registrar_invernadero.html', {
            'form' : formulario_invernadero
        })
    elif request.method=="POST":
            return render (request, 'registrar_invernadero.html', {
            'form' : formulario_invernadero
        })