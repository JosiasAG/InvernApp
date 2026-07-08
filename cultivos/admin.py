from django.contrib import admin

from cultivos.models import Cama, Cultivo, Invernadero, LoteCultivo, TareaProgramada, Zona

admin.site.register(Cultivo)
admin.site.register(LoteCultivo)
admin.site.register(TareaProgramada)
admin.site.register(Invernadero)
admin.site.register(Zona)
admin.site.register(Cama)
