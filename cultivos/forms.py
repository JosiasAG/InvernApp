from django.forms import ModelForm, DateInput, Select, TextInput
from .models import LoteCultivo, Cultivo, Invernadero, Bloque, Cama
from django import forms

class formulario_nuevo_lote(ModelForm):
    class Meta:
        model = LoteCultivo
        fields = "__all__"

        widgets = {
            'fecha_plantacion': DateInput(
                attrs= {'type': 'date'}
                ),
            }

class formulario_elegir_siembra(ModelForm):
    class Meta:
        model = Cultivo
        fields = ['tipo_cultivo']

class formulario_cultivo_tierra(ModelForm):
    class Meta:
        model = Cultivo
        exclude = [
            'ph_optimo_min', 
            'ph_optimo_max', 
            'conductividad_electrica_optima', 
            'tiempo_riego_minutos',
            'tiempo_espera_minutos'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_cultivo'].initial = 'TIERRA'
        self.fields['tipo_cultivo'].widget = forms.HiddenInput()

class formulario_cultivo_hidroponia(ModelForm):
    class Meta:
        model = Cultivo
        exclude = [
            'dias_para_primer_riego', 
            'frecuencia_riego', 
            'dias_para_primer_fertilizacion',
            'frecuencia_fertilizacion'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_cultivo'].initial = 'HIDROPONIA'
        self.fields['tipo_cultivo'].widget = forms.HiddenInput()

class formulario_cultivo_mixto(ModelForm):
    class Meta:
        model = Cultivo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_cultivo'].initial = 'TIERRA'
        self.fields['tipo_cultivo'].widget = forms.HiddenInput()

class formulario_invernadero(ModelForm):
    class Meta:
        model = Invernadero
        fields = '__all__'

class formulario_bloque(ModelForm):
    class Meta:
        model = Bloque
        fields = '__all__'
