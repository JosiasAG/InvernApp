from django.contrib import admin

from cultivos.models import Cama, CatalogoInsumos, Cultivo, Insumo, Invernadero, LoteCultivo, Proveedor, TareaProgramada, UsoInsumo, Bloque, Fumigacion
from usuarios.models import AsistenciaDiaria, PerfilEmpleado

admin.site.register(Cultivo)
admin.site.register(LoteCultivo)
admin.site.register(TareaProgramada)
admin.site.register(Invernadero)
admin.site.register(Bloque)
admin.site.register(Cama)
admin.site.register(Insumo)
admin.site.register(Fumigacion)
admin.site.register(UsoInsumo)
admin.site.register(Proveedor)
admin.site.register(CatalogoInsumos)
admin.site.register(AsistenciaDiaria)
admin.site.register(PerfilEmpleado)