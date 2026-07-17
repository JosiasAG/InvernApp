from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Cultivo(models.Model):
    nombre = models.CharField(max_length=100)
    dias_para_primer_riego = models.IntegerField()
    dias_para_primera_poda = models.IntegerField()
    dias_para_primer_fertilizacion = models.IntegerField(default=0) 
    dias_para_primer_fumigacion = models.IntegerField()
    dias_para_inicio_cosecha = models.IntegerField()
    ciclo_de_vida_total = models.IntegerField()
    frecuencia_riego = models.IntegerField(default=0) 
    frecuencia_poda = models.IntegerField(default=0) 
    frecuencia_fertilizacion = models.IntegerField(default=0)
    frecuencia_fumigacion = models.IntegerField(default = 0)
    frecuencia_cosecha = models.IntegerField(default=0)
    fecha_trasplante = models.IntegerField(default=0)
    inicio_tutorado = models.IntegerField(default=0)
    dias_para_tutorado = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class LoteCultivo(models.Model):
    id_lote = models.CharField(max_length=100)
    plantilla = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    fecha_plantacion = models.DateField()
    estado = models.CharField(max_length=50, choices=[('CRECIMIENTO', 'En crecimiento'), ('COSECHA', 'En cosecha'), ('TERMINADO', 'Terminado')], default='CRECIMIENTO')
    invernadero = models.ForeignKey('Invernadero', on_delete=models.SET_NULL, null=True, blank=True)
    bloque = models.ForeignKey('Bloque', on_delete=models.SET_NULL, null=True, blank=True)
    cama = models.ForeignKey('Cama', on_delete=models.SET_NULL, null=True, blank=True)
    SISTEMAS_CULTIVO = [
        ('HIDROPONICO', 'Hidroponía (Sustrato / Solución Recirculante)'),
        ('TRADICIONAL', 'Tradicional (Suelo / Tierra)'),
        ('MIXTO', 'Apto para ambos (Hidroponía y Tradicional)'),
    ]
    sistema_cultivo = models.CharField(max_length=20, choices=SISTEMAS_CULTIVO, default='TRADICIONAL')

    def __str__(self):
        return f"Lote {self.id_lote} - {self.plantilla.nombre}"

class TareaProgramada(models.Model):
    TIPO_ACTIVIDAD = [
        ('SIEMBRA', 'Siembra'),
        ('RIEGO', 'Riego'),
        ('FUMIGACION', 'Fumigación'),
        ('FERTILIZACION', 'Fertilización'),
        ('PODA', 'Poda / Deshije'),
        ('TUTORADO', 'Tutorado / Amarre'),
        ('TRASPLANTE', 'Trasplante'),
        ('COSECHA', 'Cosecha'),
    ]
    lote_cultivo = models.ForeignKey('LoteCultivo', on_delete=models.CASCADE)
    tipo_tarea = models.CharField(max_length=50, choices=TIPO_ACTIVIDAD)
    fecha_programada = models.DateField()
    completada = models.BooleanField(default=False)
    insumo_utilizado = models.ForeignKey('Insumo', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    duracion_tarea = models.DurationField(null=True, blank=True)
    invernadero = models.ForeignKey('Invernadero', on_delete=models.SET_NULL, null=True, blank=True)
    bloque = models.ForeignKey('Bloque', on_delete=models.SET_NULL, null=True, blank=True)
    cama = models.ForeignKey('Cama', on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"Tarea {self.tipo_tarea} para {self.lote_cultivo.id_lote} programada para {self.fecha_programada}"

class Invernadero(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    cantidad_bloques = models.IntegerField()

    def __str__(self):
        return self.nombre

class Bloque(models.Model):
    nombre = models.CharField(max_length=100)
    invernadero = models.ForeignKey(Invernadero, on_delete=models.CASCADE, related_name="bloques")
    descripcion = models.TextField(blank=True, null=True)
    cantidad_camas = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.invernadero.nombre}" 
    
class Cama(models.Model):
    numero_cama = models.IntegerField(default=0)
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, null=True)
    descripcion = models.TextField(blank=True, null=True)
    disponibilidad = models.CharField(max_length=50, choices=[('DISPONIBLE', 'Disponible'), ('OCUPADA', 'Ocupada')], default='DISPONIBLE')

    def __str__(self):
        return f"{self.numero_cama} - {self.bloque.nombre}"
    
class Insumo(models.Model):
    nombre = models.ForeignKey('CatalogoInsumos', on_delete=models.CASCADE)
    lote = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, related_name='catalogo_insumos', default=None, null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=[('FERTILIZANTE', 'Fertilizante'), ('PLAGUICIDA', 'Plaguicida'), ('SEMILLA', 'Semilla'), ('SUSTRATO', 'Sustrato'), ('OTRO', 'Otro')], default='-----')
    descripcion = models.TextField(blank=True, null=True)
    cantidad_disponible = models.FloatField()
    cantidad_minima = models.FloatField(default=0.0)
    

    def __str__(self):
        return self.nombre.nombre
    
class UsoInsumo(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    dosis_por_cama = models.FloatField()

    def __str__(self):
        return f"{self.insumo.nombre} para {self.cultivo.nombre}"
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class CatalogoInsumos(models.Model):
    tipo_insumo = models.CharField(max_length=50, choices=[('FERTILIZANTE', 'Fertilizante'), ('PLAGUICIDA', 'Plaguicida'), ('SEMILLA', 'Semilla'), ('SUSTRATO', 'Sustrato'), ('OTRO', 'Otro')])
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50, choices=[('KG', 'Kilogramos'), ('L', 'Litros'), ('UNIDAD', 'Unidad'), ('BULTOS', 'Bultos')])


    def __str__(self):
        return f"{self.nombre}"
    
class Fumigacion(models.Model):
    bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE, related_name='fumigaciones')
    fecha_aplicacion = models.DateTimeField(default=timezone.now())
    compuesto_aplicado = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    # dosis = models.IntegerField(default=0, help_text="expresado en gramos o mililitros")
    gasto_agua = models.FloatField(help_text="Litros de agua totales preparados")
    intervalo_seguridad = models.IntegerField(
        help_text="Días obligatorios que deben pasar antes de poder cosechar"
    )
    plaga_objetivo = models.CharField(max_length=100)
    aplicador = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)

    @property
    def periodo_espera_activo(self):
        fecha_limite = self.fecha_aplicacion.date() + models.fields.DateTimeField.timedelta(days=self.intervalo_seguridad)
        return timezone.now() < fecha_limite