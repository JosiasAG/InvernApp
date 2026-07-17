from django.utils import timezone

from django.shortcuts import render, redirect
from .models import Cultivo, LoteCultivo, TareaProgramada, Invernadero, Bloque, Cama, Insumo, UsoInsumo, Proveedor, CatalogoInsumos
from .forms import formulario_nuevo_lote, formulario_cultivo, formulario_invernadero, formulario_bloque

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
        form.save(commit=False)
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
    if request.method == "GET":

        return render(request, 'registrar_invernadero.html', {
            'form': formulario_invernadero()
        }) 
    elif request.method == "POST" and 'guardar_invernadero':
        form = formulario_invernadero(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registrar_bloque.html')
        
from django.shortcuts import render, redirect
from .models import Invernadero, Bloque
from .forms import formulario_bloque # Asegúrate de importar tu formulario

def registrar_bloque(request):
    if request.method == "POST":
        if 'abrir_invernadero' in request.POST:
            id_invernadero = request.POST.get('invernadero')
            form_con_seleccion = formulario_bloque(request.POST) 
            bloques_asociados = None
            if id_invernadero:
                invernadero_objeto = Invernadero.objects.get(id=id_invernadero)
                bloques_asociados = invernadero_objeto.bloques.all()
            return render(request, 'registrar_bloque.html', {
                'form': form_con_seleccion,
                'bloques': bloques_asociados,
            })
        elif 'guardar_bloque' in request.POST:
            bloque_ids = request.POST.getlist('bloque_ids')
            for b_id in bloque_ids:
                cantidad_camas = request.POST.get(f'camas_{b_id}')
                descripcion = request.POST.get(f'descripcion_{b_id}') # Agregado para guardar la descripción
                if cantidad_camas:
                    bloque = Bloque.objects.get(id=b_id)
                    bloque.cantidad_camas = int(cantidad_camas)
                    bloque.descripcion = descripcion # Lo guardamos en el modelo
                    bloque.save()
            return redirect('home')
    else:
        return render(request, 'registrar_bloque.html', {
            'form': formulario_bloque(),
        })

def crear_cultivo(request):
    return render (request, '')