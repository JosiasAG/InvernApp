from django.contrib import admin

from cultivos.models import Cama, CatalogoInsumos, Cultivo, Insumo, Invernadero, LoteCultivo, Proveedor, TareaProgramada, UsoInsumo, Zona

admin.site.register(Cultivo)
admin.site.register(LoteCultivo)
admin.site.register(TareaProgramada)
admin.site.register(Invernadero)
admin.site.register(Zona)
admin.site.register(Cama)
admin.site.register(Insumo)
admin.site.register(UsoInsumo)
admin.site.register(Proveedor)
admin.site.register(CatalogoInsumos)
