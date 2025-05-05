from django import forms
from models import Persona

class LoginForm(forms.Form):
    rut = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Rut'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 's_nombre', 'apellido', 's_apellido', 'rut', 'dv', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'password', 're_password']
        widgets = {
            'nombre': forms.CharField(attrs={'placeholder': 'Nombre'}),
            's_nombre': forms.TextInput(attrs={'placeholder': 'Segundo Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            's_apellido': forms.TextInput(attrs={'placeholder': 'Apellido Materno'}),
            'rut': forms.TextInput(attrs={'placeholder': 'Rut'}),
            'dv': forms.TextInput(attrs={'placeholder': 'DV'}),
            'fecha_nacimiento': forms.DateInput(attrs={'placeholder': 'Fecha de Nacimiento', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            're_password': forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña'}),


        } 