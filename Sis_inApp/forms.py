from django import forms
from .models import Alumnos, Grupos

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = ['nombre', 'numero_control', 'id_grupo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_control': forms.TextInput(attrs={'class': 'form-control'}),
            'id_grupo': forms.Select(attrs={'class': 'form-select'})
        }

class ReinscripcionForm(forms.Form):
    alumno = forms.ModelChoiceField(
        queryset=Alumnos.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    nuevo_grupo = forms.ModelChoiceField(
        queryset=Grupos.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )