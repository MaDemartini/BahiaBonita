# BahiaBonita
ya mi gente, comenzamos con el proeycto, traten de ir dejando una bitacora de avance el el redme y en lo posible con fotos y lo mas explicativo posible


## API Interna - Información de Departamentos

EAPI REST construida con Django Rest Framework, permite consultar información detallada de los departamentos del edificio Bahía Bonita.

Endpoints disponibles:

- `GET /api/depto/disponibles/` → Lista solo los departamentos disponibles (no en mantenimiento).
- `GET /api/depto/todos/` → Lista todos los departamentos, sin importar su estado.

Uso común:
- Integración con el sitio web para mostrar departamentos disponibles a clientes.
- Consulta administrativa para ver todos los departamentos (uso interno).
