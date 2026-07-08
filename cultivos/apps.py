from django.apps import AppConfig


class CultivosConfig(AppConfig):
    name = 'cultivos'
    
    def ready(self):
        import cultivos.signals
