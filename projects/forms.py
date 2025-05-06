from django import forms
from django.core.exceptions import ValidationError
from .models import Persona

class LoginForm(forms.Form):
    rut = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Rut'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 's_nombre', 'apellido', 's_apellido', 'rut', 'dv', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'password', 're_password']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            's_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo nombre'}),
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

#funcion para validar rut y dv
def clean():
    cleaned_data = super().clean()
    rut = cleaned_data.get('rut')
    dv = cleaned_data.get('dv')
    if not rut or not dv:
        raise ValidationError("El RUT y el dígito verificador son obligatorios.")
    print(f"RUT: {rut}, DV: {dv}")  # Agrega un log para verificar los valores      

    if not rut.isdigit():
        raise ValidationError("El RUT debe contener solo números.")

    if not validar_dv(rut, dv):  # Ahora `validar_dv` está definido
        raise ValidationError("El dígito verificador no es válido.")

    return cleaned_data

def validar_dv(rut: str, dv: str) -> bool:
    suma = 0
    multiplo = 2

    for c in reversed(rut):
        suma += int(c) * multiplo
        multiplo = 9 if multiplo == 7 else multiplo + 1

    resto = suma % 11
    dv_esperado = 11 - resto

    if dv_esperado == 11:
        dv_esperado = "0"
    elif dv_esperado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_esperado)

    return dv.upper() == dv_esperado