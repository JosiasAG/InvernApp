from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Insumo, LoteCultivo, TareaProgramada, UsoInsumo
from datetime import timedelta

@receiver(post_save, sender=LoteCultivo)
def crear_calendario_lote(sender, instance, created, **kwargs):
    if created:
        fecha_base = instance.fecha_plantacion
        plantilla = instance.plantilla
        for i in range(0, plantilla.ciclo_de_vida_total, plantilla.frecuencia_riego):
            fecha_tarea = fecha_base + timedelta(days=i)
            TareaProgramada.objects.create(
                lote_cultivo=instance,
                tipo_tarea='RIEGO',
                fecha_programada=fecha_tarea
            )

        for i in range(plantilla.dias_para_primera_poda, plantilla.ciclo_de_vida_total, plantilla.frecuencia_poda):
            fecha_tarea = fecha_base + timedelta(days=i)
            TareaProgramada.objects.create(
                lote_cultivo=instance,
                tipo_tarea='PODA',
                fecha_programada=fecha_tarea
            )

        for i in range(plantilla.dias_para_primer_fertilizacion, plantilla.ciclo_de_vida_total, plantilla.frecuencia_fertilizacion):  # Suponiendo fertilización cada 30 días
            fecha_tarea = fecha_base + timedelta(days=i)
            TareaProgramada.objects.create(
                lote_cultivo=instance,
                tipo_tarea='FERTILIZACION',
                fecha_programada=fecha_tarea
            )

        for i in range(plantilla.dias_para_inicio_cosecha, plantilla.ciclo_de_vida_total, plantilla.frecuencia_cosecha):  # Suponiendo cosecha cada 30 días
            fecha_tarea = fecha_base + timedelta(days=i)
            TareaProgramada.objects.create(
                lote_cultivo=instance,
                tipo_tarea='COSECHA',
                fecha_programada=fecha_tarea
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