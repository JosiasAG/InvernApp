from django.db import models

class Cultivo(models.Model):
    nombre = models.CharField(max_length=100)
    dias_para_primer_riego = models.IntegerField()
    dias_para_primera_poda = models.IntegerField()
    dias_para_primer_fertilizacion = models.IntegerField(default=0)  # Suponiendo fertilización cada 30 días
    dias_para_inicio_cosecha = models.IntegerField()
    ciclo_de_vida_total = models.IntegerField()
    frecuencia_riego = models.IntegerField(default=0) 
    frecuencia_poda = models.IntegerField(default=0) 
    frecuencia_fertilizacion = models.IntegerField(default=0)
    frecuencia_cosecha = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class LoteCultivo(models.Model):
    id_lote = models.CharField(max_length=100)
    plantilla = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    fecha_plantacion = models.DateField()
    estado = models.CharField(max_length=50, choices=[('CRECIMIENTO', 'En crecimiento'), ('COSECHA', 'En cosecha'), ('TERMINADO', 'Terminado')], default='CRECIMIENTO')
    cama = models.ForeignKey('Cama', on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Lote {self.id_lote} - {self.plantilla.nombre}"

class TareaProgramada(models.Model):
    lote_cultivo = models.ForeignKey(LoteCultivo, on_delete=models.CASCADE)
    tipo_tarea = models.CharField(max_length=50, choices=[('RIEGO', 'Riego'), ('PODA', 'Poda'), ('FERTILIZACION', 'Fertilización'), ('COSECHA', 'Cosecha')])
    fecha_programada = models.DateField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Tarea {self.tipo_tarea} para {self.lote_cultivo.id_lote} programada para {self.fecha_programada}"
    
class Invernadero(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    invernadero = models.ForeignKey(Invernadero, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.invernadero.nombre}" 
    
class Cama(models.Model):
    numero_cama = models.IntegerField()
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    disponibilidad = models.CharField(max_length=50, choices=[('DISPONIBLE', 'Disponible'), ('OCUPADA', 'Ocupada')], default='DISPONIBLE')

    def __str__(self):
        return f"{self.numero_cama} - {self.zona.nombre}"