from .models import Administrador, Recepcionista, PersonalAseo

MODELOS_POR_ROL = {
    'Administrador': {
        'modelo': Administrador,
        'campos': ['fotoAdministrador', 'profesion', 'cert_antecedentes', 'prevision']
    },
    'Recepcionista': {
        'modelo': Recepcionista,
        'campos': ['turno', 'sueldo']
    },
    'Personal Aseo': {
        'modelo': PersonalAseo,
        'campos': ['area', 'tipo_contrato']
    }
}