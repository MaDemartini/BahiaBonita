from django import forms
from django.core.exceptions import ValidationError
from .models import Contacto, Persona, Departamento, Reserva
from .utils import validar_dv  # Asegúrate de tener esta función implementada
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'})
    )

class RegisterForm(forms.ModelForm):

    re_password = forms.CharField(label='Confirmar Contraseña', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirmar Contraseña'}))

    class Meta:
        model = Persona
        fields = ['rol','nombre', 's_nombre', 'apellido', 's_apellido', 'rut', 'dv', 'fecha_nacimiento', 'direccion', 'pais',
                  'ciudad', 'telefono', 'email', 'password']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control', 'id': 'rol'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            's_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellido'}),
            's_apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellido Materno'}),
            'rut': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Rut'}),
            'dv': forms.TextInput(attrs={'class': 'form-control','placeholder': 'DV'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de Nacimiento', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Dirección'}),
            'pais' : forms.TextInput(attrs={'class': 'form-control', 'id': 'pais'}),
            'ciudad' : forms.TextInput(attrs={'class': 'form-control', 'id': 'ciudad'}),            
            'telefono': forms.TextInput(attrs={'class': 'form-control','value': '+569'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Contraseña'}),

        } 

#funcion para validar rut y dv
#se valida el rut incorrecto pero hay que agregar las alertas
    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get('rut')
        dv = cleaned_data.get('dv')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if not rut or not dv:
            self.add_error('rut', "El RUT y el dígito verificador son obligatorios.")
            return cleaned_data    

        if not rut.isdigit():
            self.add_error('rut', "El RUT debe contener solo números.")

        if not validar_dv(rut, dv):  # type: ignore
            self.add_error('dv', "El dígito verificador no es válido.")

        if password and re_password and password != re_password:
            self.add_error('re_password', "Las contraseñas no coinciden.")

        return cleaned_data     


        
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['departamento', 'fecha_ingreso', 'fecha_salida', 'cant_personas']

    def clean(self):
        cleaned_data = super().clean()
        fecha_ingreso = cleaned_data.get('fecha_ingreso')
        fecha_salida = cleaned_data.get('fecha_salida')
        departamento = cleaned_data.get('departamento')

        if fecha_ingreso and fecha_salida:
            if fecha_salida <= fecha_ingreso:
                raise forms.ValidationError("La fecha de salida debe ser mayor que la fecha de ingreso.")
            if (fecha_salida - fecha_ingreso).days < 1:
                raise forms.ValidationError("La reserva debe ser al menos de un día.")

            # Validar bloqueo temporal (fecha ya reservada)
            from .models import Reserva
            overlapping_reservas = Reserva.objects.filter(
                departamento=departamento,
                fecha_salida__gt=fecha_ingreso,
                fecha_ingreso__lt=fecha_salida,
            )
            if overlapping_reservas.exists():
                raise forms.ValidationError("El departamento está reservado en las fechas seleccionadas.")

            # Validar que no sea mensual desde aquí (por ejemplo >30 días)
            dias_reserva = (fecha_salida - fecha_ingreso).days
            if dias_reserva > 30:
                raise forms.ValidationError(
                    "Reservas mensuales no están disponibles en la web. Por favor en contacto contacte a administración."
                )
        return cleaned_data

# clase para administracion, crear departamentos en la db
class AddDeptoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['num_depto','cant_dormitorios','cant_banos','piso','cant_personas','imagen','valor_dia','mantenimiento']
        widgets = {
            'cant_dormitorios': forms.NumberInput(attrs={'placeholder': 'Cantidad de dormitorios'}),
            'cant_banos': forms.NumberInput(attrs={'placeholder': 'Cantidad de baños'}),
            'piso': forms.NumberInput(attrs={'placeholder': 'Piso'}),
            'cant_personas': forms.NumberInput(attrs={'placeholder': 'Cantidad de personas'}),
            'imagen': forms.TextInput(attrs={'placeholder': 'Imagen'}),
            'valor_dia': forms.NumberInput(attrs={'placeholder': 'Valor por día'}),
            'mantenimiento': forms.CheckboxInput(),
        }
    
    
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mensaje'}),
        }