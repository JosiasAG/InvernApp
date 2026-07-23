from django.forms import ModelForm, DateInput, Select, TextInput
from .models import LoteCultivo, Cultivo, Invernadero, Bloque, Cama
from django import forms

class formulario_nuevo_lote(forms.ModelForm):
    class Meta:
        model = LoteCultivo
        fields = ['id_lote', 'plantilla', 'tipo_sustrato_sugerido', 'estado', 'invernadero', 'bloque', 'cama']
        
        widgets = {
            'invernadero': forms.Select(attrs={'id': 'select-invernadero', 'onchange': 'filtrarBloques()'}),
            'bloque': forms.Select(attrs={'id': 'select-bloque', 'onchange': 'filtrarCamas()'}),
            'cama': forms.Select(attrs={'id': 'select-cama'}),
            'fecha_plantacion': DateInput(attrs= {'type': 'date'}),
        }

class formulario_elegir_siembra(ModelForm):
    class Meta:
        model = Cultivo
        fields = ['tipo_cultivo']

class formulario_cultivo_tierra(ModelForm):
    class Meta:
        model = Cultivo
        exclude = [
            'fecha_trasplante',
            'ph_optimo_min', 
            'ph_optimo_max', 
            'conductividad_electrica_optima',
            'frecuencia_monitoreo_ph_ce',
        ]
        widgets = {
            'fecha_plantacion': DateInput(attrs= {'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_cultivo'].initial = 'TIERRA'
        self.fields['tipo_cultivo'].widget = forms.HiddenInput()

class formulario_cultivo_hidroponia(ModelForm):
    class Meta:
        model = Cultivo
        exclude = [
            'fecha_trasplante',
            'primer_riego', 
            'frecuencia_riego', 
            'primer_fertilizacion',
            'frecuencia_fertilizacion'
        ]

        widgets = {
            'fecha_plantacion': DateInput(attrs= {'type': 'date'}),
            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_cultivo'].initial = 'HIDROPONIA'
        self.fields['tipo_cultivo'].widget = forms.HiddenInput()

class formulario_cultivo_mixto(ModelForm):
    class Meta:
        model = Cultivo
        fields = '__all__'
        exclude = ['fecha_trasplante']

        widgets = {
        'fecha_plantacion': DateInput(attrs= {'type': 'date'}),
        }

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
