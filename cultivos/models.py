from django.db import models

class Cultivo(models.Model):
    nombre = models.CharField(max_length=100)
    dias_para_primer_riego = models.IntegerField()
    dias_para_primera_poda = models.IntegerField()
    dias_para_inicio_cosecha = models.IntegerField()
    ciclo_de_vida_total = models.IntegerField()
    frecuencia_riego = models.IntegerField()
    frecuencia_poda = models.IntegerField()

    def __str__(self):
        return self.nombre

class LoteCultivo(models.Model):
    id_lote = models.CharField(max_length=100)
    plantilla = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    fecha_plantacion = models.DateField()
    estado = models.CharField(max_length=50, choices=[('CRECIMIENTO', 'En crecimiento'), ('COSECHA', 'En cosecha'), ('TERMINADO', 'Terminado')], default='CRECIMIENTO')

    def __str__(self):
        return f"Lote {self.id_lote} - {self.plantilla.nombre}"

class TareaProgramada(models.Model):
    lote_cultivo = models.ForeignKey(LoteCultivo, on_delete=models.CASCADE)
    tipo_tarea = models.CharField(max_length=50, choices=[('RIEGO', 'Riego'), ('PODA', 'Poda'), ('FERTILIZACION', 'Fertilización'), ('COSECHA', 'Cosecha')])
    fecha_programada = models.DateField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Tarea {self.tipo_tarea} para {self.lote_cultivo.id_lote} programada para {self.fecha_programada}"