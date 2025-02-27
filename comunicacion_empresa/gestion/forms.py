# gestion/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Proyecto, Tarea, Mensaje, Comentario

# gestion/forms.py
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'usuarios']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'usuarios': forms.CheckboxSelectMultiple(),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_limite', 'estado', 'asignados']
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido', 'destinatarios']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']