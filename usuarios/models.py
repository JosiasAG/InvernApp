from django.db import models
from django.contrib.auth.models import AbstractUser
from InverApp import settings

class Usuario(AbstractUser):
    pass

class PerfilEmpleado(models.Model):
    ROLES = [
        ('ADMINISTRADOR', 'Administrador / Agrónomo'),
        ('OPERARIO', 'Operario de Campo'),
        ('SUPERVISOR', 'Supervisor de Zona'),
    ]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='OPERARIO')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    hora_entrada_establecida = models.TimeField(default="08:00:00")
    hora_salida_establecida = models.TimeField(default="16:00:00")
    
    esta_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
class AsistenciaDiaria(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha}"