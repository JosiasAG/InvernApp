from django.db.models.signals import post_save
from django.dispatch import receiver
from usuarios.models import Usuario, PerfilEmpleado


@receiver(post_save, sender=Usuario)
def crear_perfil_usuario_automatico(sender, instance, created, **kwargs):
    if created:
        PerfilEmpleado.objects.create(usuario=instance)