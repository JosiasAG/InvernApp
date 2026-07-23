from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Insumo, LoteCultivo, TareaProgramada, UsoInsumo, Invernadero, Bloque, Cama
from datetime import timedelta, timezone
from usuarios.models import AsistenciaDiaria

@receiver(post_save, sender=LoteCultivo)
def crear_calendario_lote(sender, instance, created, **kwargs):
    if not created:
        return
    else:
        fecha_base = instance.fecha_plantacion
        plantilla = instance.plantilla
        ciclo_vida = plantilla.ciclo_vida_total
        dias_trasplante = plantilla.dias_para_trasplante if plantilla.requiere_trasplante and plantilla.dias_para_trasplante else 0
        fecha_trasplante = fecha_base + timedelta(days=dias_trasplante)
        # tareas de riego
        if plantilla.tipo_cultivo in ["TIERRA", 'MIXTO']:
            for i in range(0, ciclo_vida, plantilla.frecuencia_riego):
                fecha_tarea = fecha_base + timedelta(days=i)
                TareaProgramada.objects.create(
                    lote_cultivo=instance,
                    tipo_tarea='RIEGO',
                    fecha_programada=fecha_tarea,
                    invernadero=instance.invernadero,
                    bloque=instance.bloque,
                    cama=instance.cama,
                )
        #tareas de poda
        if plantilla.tipo_cultivo in ["TIERRA", 'MIXTO', 'HIDROPONIA'] and plantilla.requiere_poda:
            for i in range(0, ciclo_vida, plantilla.frecuencia_poda):
                fecha_tarea = fecha_trasplante + timedelta(days=i)
                TareaProgramada.objects.create(
                    lote_cultivo=instance,
                    tipo_tarea='PODA',
                    fecha_programada=fecha_tarea,
                    invernadero=instance.invernadero,
                    bloque=instance.bloque,
                    cama=instance.cama,
                )

        # tareas de tutorado
        if plantilla.tipo_cultivo in ["TIERRA", 'MIXTO', 'HIDROPONIA'] and plantilla.requiere_tutorado:
            for i in range(0, ciclo_vida, plantilla.frecuencia_tutorado): 
                fecha_tarea = fecha_trasplante + timedelta(days=i)
                TareaProgramada.objects.create(
                    lote_cultivo=instance,
                    tipo_tarea='TUTORADO',
                    fecha_programada=fecha_tarea,
                    invernadero=instance.invernadero,
                    bloque=instance.bloque,
                    cama=instance.cama,
                )

        #traeas de fertilización
        if plantilla.tipo_cultivo in ["TIERRA", 'MIXTO']:
                for i in range(0, ciclo_vida, plantilla.frecuencia_fertilizacion): 
                    fecha_tarea = fecha_trasplante + timedelta(days=i)
                    TareaProgramada.objects.create(
                        lote_cultivo=instance,
                        tipo_tarea='FERTILIZACION',
                        fecha_programada=fecha_tarea,
                        invernadero=instance.invernadero,
                        bloque=instance.bloque,
                        cama=instance.cama,
                    )

        # tareas de monitoreo
        if plantilla.tipo_cultivo in ["HIDROPONIA", "MIXTO"] and plantilla.frecuencia_monitoreo_ph_ce:
            for i in range(0, ciclo_vida, plantilla.frecuencia_monitoreo_ph_ce):
                fecha_tarea = fecha_trasplante + timedelta(days=i)
                TareaProgramada.objects.create(
                    lote_cultivo=instance,
                    tipo_tarea='MONITOREO',
                    fecha_programada=fecha_tarea,
                    invernadero=instance.invernadero,
                    bloque=instance.bloque,
                    cama=instance.cama,
                )

        # tareas de trasplante (y orden de prepareación)
        if plantilla.requiere_trasplante and plantilla.dias_para_trasplante:
            dias_preparacion_antes_trasplante = 5
            dias_preparacion = max(0, plantilla.dias_para_trasplante - dias_preparacion_antes_trasplante)
            fecha_preparacion = fecha_base + timedelta(days=dias_preparacion)
            
            TareaProgramada.objects.create(
                lote_cultivo=instance,
                tipo_tarea='ACONDICIONAMIENTO',
                fecha_programada=fecha_preparacion,
                invernadero=instance.invernadero,
                bloque=instance.bloque,
                cama=instance.cama,
            )
            TareaProgramada.objects.create(
                lote_cultivo=instance,
                tipo_tarea='TRASPLANTE',
                fecha_programada=fecha_trasplante,
                invernadero=instance.invernadero,
                bloque=instance.bloque,
                cama=instance.cama,
            )

        # tareas de cosecha
        if plantilla.frecuencia_cosecha and plantilla.primera_cosecha:
            primera_cosecha = plantilla.primera_cosecha
            for i in range(primera_cosecha, ciclo_vida, plantilla.frecuencia_cosecha):
                fecha_tarea = fecha_base + timedelta(days=i)
                TareaProgramada.objects.create(
                    lote_cultivo=instance,
                    tipo_tarea='COSECHA',
                    fecha_programada=fecha_tarea,
                    invernadero=instance.invernadero,
                    bloque=instance.bloque,
                    cama=instance.cama,
                )

@receiver(post_save, sender=LoteCultivo)
def actualizar_disponibilidad_cama(sender, instance, created, **kwargs):
    if instance.cama:
        cama_estado = instance.estado
        if created:
            instance.cama.disponibilidad = 'OCUPADA'
            instance.cama.save()
        else:
            if cama_estado == 'TERMINADO':
                instance.cama.disponibilidad = 'DISPONIBLE'
                instance.cama.save()

@receiver(post_save, sender=TareaProgramada)
def descontar_inventario_por_tarea(sender, instance, created, **kwargs):
    if instance.completada and instance.tipo_tarea == 'FERTILIZACION':
        cantidad_camas_fertilizadas = 1
        dosis_a_usar = UsoInsumo.objects.filter(
            cultivo=instance.lote_cultivo.plantilla, 
            insumo=instance.insumo_utilizado
        ).first()
        dosis_total = dosis_a_usar.dosis_por_cama * cantidad_camas_fertilizadas
        instance.insumo_utilizado.cantidad_disponible -= dosis_total
        instance.insumo_utilizado.save()

@receiver(post_save, sender=TareaProgramada)
def calcular_linea_tiempo_y_descuento(sender, instance, created, **kwargs):
    if instance.completada and not instance.fecha_completada:
        ahora = timezone.now()
        hoy = ahora.date()
        usuario = instance.usuario_asignado

        if usuario:
            ultima_tarea = TareaProgramada.objects.filter(
                usuario_asignado=usuario,
                completada=True,
                fecha_completada__date=hoy
            ).exclude(id=instance.id).order_by('-fecha_completada').first()

            if ultima_tarea:
                punto_inicio = ultima_tarea.fecha_completada
            else:
                asistencia = AsistenciaDiaria.objects.filter(usuario=usuario, fecha=hoy).first()
                if asistencia and asistencia.hora_entrada:
                    punto_inicio = asistencia.hora_entrada
                else:
                    punto_inicio = timezone.make_aware(
                        timezone.datetime.combine(hoy, timezone.datetime.min.time().replace(hour=8))
                    )

            duracion = ahora - punto_inicio
            TareaProgramada.objects.filter(id=instance.id).update(
                fecha_completada=ahora,
                duracion_tarea=duracion
            )

@receiver(post_save, sender=Invernadero)
def establecer_invernadero(sender, instance, created, **kwargs):
    cantidad_bloques=instance.cantidad_bloques
    if created:
        for i in "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"[:cantidad_bloques]:                
                Bloque.objects.create(
                    nombre = "Bloque " + i,
                    invernadero = instance,
                    descripcion = "",
                    cantidad_camas = 0,
                )

@receiver(post_save, sender=Bloque)
def establecer_bloque(sender, instance, created, **Kwargs):
    cantidad_camas=instance.cantidad_camas
    for i in range(1, cantidad_camas+1):                
                Cama.objects.create(
                    numero_cama = i,
                    bloque = instance,
                    descripcion = "",
                    disponibilidad = 'DISPONIBLE'
                )



