from django.forms import ModelForm, DateInput, Select, TextInput
from .models import LoteCultivo

class formulario_nuevo_lote(ModelForm):
    class Meta:
        model = LoteCultivo
        fields = "__all__"

        widgets = {
            'fecha_plantacion': DateInput(
                attrs= {'type': 'date'}
                ),
            }