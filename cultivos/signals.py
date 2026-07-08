from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LoteCultivo, TareaProgramada
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