from django.forms import ModelForm, DateInput, Select, TextInput
from .models import LoteCultivo, Cultivo, Invernadero, Bloque, Cama

class formulario_nuevo_lote(ModelForm):
    class Meta:
        model = LoteCultivo
        fields = "__all__"

        widgets = {
            'fecha_plantacion': DateInput(
                attrs= {'type': 'date'}
                ),
            }
        
class formulario_cultivo(ModelForm):
    class Meta:
        model = Cultivo
        fields = '__all__'

class formulario_invernadero(ModelForm):
    class Meta:
        model = Invernadero
        fields = '__all__'

