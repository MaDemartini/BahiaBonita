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
#se valida el rut incorrecto pero hay que agregar las alertas
        def clean(self):
            cleaned_data = super().clean()
            rut = cleaned_data.get('rut')
            dv = cleaned_data.get('dv')
            if not rut or not dv:
                self.add_error("El RUT y el dígito verificador son obligatorios.")
                return cleaned_data    

            if not rut.isdigit():
                self.add_error('rut', "El RUT debe contener solo números.")

            if not validar_dv(rut, dv):  # type: ignore # Ahora `validar_dv` está definido
                self.add_error('dv', "El dígito verificador no es válido.")

            if password and re_password and password != re_password:
                self.add_error('re_password', "Las contraseñas no coinciden.")

            return cleaned_data

        
class ReservaForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    cantidad_de_personas = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'placeholder': 'Cantidad de personas'}))
    tipo_de_reserva = forms.ChoiceField(choices=[('diaria', 'Diaria'), ('mensual', 'Mensual')], widget=forms.Select(attrs={'class': 'form-control'}))

    