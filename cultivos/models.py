from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Cultivo(models.Model):
    tipo_cultivo = models.CharField(choices=[
        ('TIERRA', 'Tierra'),
        ('HIDROPONIA', 'Hidroponia'),
        ('MIXTO', 'Tierra e hidroponia')

    ])
    # parámetros compartidos
    nombre = models.CharField(max_length=100)
    dias_para_primera_poda = models.IntegerField()
    dias_para_inicio_cosecha = models.IntegerField()
    ciclo_de_vida_total = models.IntegerField()
    frecuencia_poda = models.IntegerField() 
    frecuencia_cosecha = models.IntegerField()
    fecha_trasplante = models.IntegerField()
    inicio_tutorado = models.IntegerField()
    dias_para_tutorado = models.IntegerField()
    
    #parametros exclusivos de tierra
    dias_para_primer_riego = models.IntegerField()
    frecuencia_riego = models.IntegerField() 
    dias_para_primer_fertilizacion = models.IntegerField()
    frecuencia_fertilizacion = models.IntegerField()

    #parametros exclusivos de hidroponia
    ph_optimo_min = models.IntegerField()
    ph_optimo_max = models.IntegerField()
    conductividad_electrica_optima = models.IntegerField()
    tiempo_riego_minutos = models.IntegerField()
    tiempo_espera_minutos = models.IntegerField()


    def __str__(self):
        return self.nombre

class LoteCultivo(models.Model):
    id_lote = models.CharField(max_length=100)
    plantilla = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    fecha_plantacion = models.DateField()
    invernadero = models.ForeignKey('Invernadero', on_delete=models.CASCADE)
    bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE)
    cama = models.ForeignKey('Cama', on_delete=models.CASCADE)
    tipo_sustrato_sugerido = models.CharField(choices=[
        ('FIBRA_COCO', 'Fibra de coco'), 
        ('PERLITA', 'Perlita'), 
        ('TEZONTLE', 'Tezontle'), 
        ('VERMICULITA', 'Vermiculita'),
        ('LANA_ROCA', 'Lana de roca'),
        ('ARCILLA_EXPANDIDA', 'Arcilla expandida'),
        ('TURBA', 'Turba'),
        ('RAIZ_FLOTANTE', 'Sin sustrato'),
        ])

    def __str__(self):
        return f"Lote {self.id_lote} + {self.plantilla.nombre}"

class TareaProgramada(models.Model):
    lote_cultivo = models.ForeignKey('LoteCultivo', on_delete=models.CASCADE, related_name="lote_cultivo")
    tipo_tarea = models.ForeignKey('LoteCultivo', on_delete=models.CASCADE, related_name="tipo_tarea")
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
    tipo = models.CharField(max_length=50, choices=[('FERTILIZANTE', 'Fertilizante'), ('SEMILLA', 'Semilla'), ('SUSTRATO', 'Sustrato'), ('OTRO', 'Otro')], default='-----')
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
    tipo_insumo = models.CharField(max_length=50, choices=[('FERTILIZANTE', 'Fertilizante'), ('SEMILLA', 'Semilla'), ('SUSTRATO', 'Sustrato'), ('OTRO', 'Otro')])
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50, choices=[('KG', 'Kilogramos'), ('L', 'Litros'), ('UNIDAD', 'Unidad'), ('BULTOS', 'Bultos')])


    def __str__(self):
        return f"{self.nombre}"
    
class Fumigacion(models.Model):
    bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE, related_name='fumigaciones')
    fecha_aplicacion = models.DateTimeField(default=timezone.now())
    compuesto_aplicado = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    dosis = models.IntegerField(default=0, help_text="expresado en gramos o mililitros")
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

class CatalogoPlagas(models.Model):
    nombre_comun = models.CharField(max_length=100)
    nombre_cientifico = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=80, choices=[('INSECTO', 'insecto'), ('ACARO', 'ácaro'), ('HONGO', 'hongo'), ('BACTERIA', 'bacteria'), ('VIRUS', 'virus')])
    descripcion_sintomas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre_comun}"
    
class CatalogoAgroquimicos(models.Model):
    nombre = models.CharField(max_length=50)
    