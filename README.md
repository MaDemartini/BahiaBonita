YA HICIMOS ENTREGA 2, AHORA VIENE LA ENTREGA 3 PRUEBAS DE SEGURIDAD Y BUGS, NO ARREGLAR FALLOS, YA TERMINO FASE 2! https://gettaurus.org/ para hacer las pruebas de seguridad, Se debe subir 1000 departamentos para poder hacer la prueba

# BahiaBonita
Aplicación para gestionar reservas, departamentos y clientes usando **Django** y **Django REST Framework**.

## Requisitos previos
- Python 3.11 o superior
- `virtualenv` para crear entornos aislados
- Node y `npm` si se desea utilizar la parte web

## Configuración del entorno

1. Clona el repositorio y crea un entorno virtual:

   ```bash
   python -m venv env
   source env/bin/activate
   ```

2. Instala las dependencias de Python:

   ```bash
   pip install -r requirements.txt
   ```

3. Si planeas usar la interfaz web instala las dependencias de JavaScript:

   ```bash
   npm install
   ```

## Migraciones y servidor

1. Aplica las migraciones para preparar la base de datos:

   ```bash
   python manage.py migrate
   ```

2. Inicia el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```
   
## Arquitectura

El código se organiza en varias capas. Las **vistas** reciben las peticiones del usuario, los **serializers** y la lógica de negocio actúan como intermediarios y los **modelos** gestionan el acceso a datos a través del ORM de Django.

```
[Cliente] --HTTP--> [Views/API] --ORM--> [Base de Datos]
   ^                                     |
   |------------- Respuesta JSON ---------|
```

Las peticiones entran a la capa de presentación y de ahí a la lógica, que consulta los modelos. El resultado vuelve al cliente como JSON o HTML según corresponda.

## Uso de la API

El proyecto ofrece varios endpoints REST bajo `/api/`. Algunos ejemplos:

- `GET /api/depto/disponibles/` &mdash; departamentos que no están en mantenimiento.
- `GET /api/depto/todos/` &mdash; lista de todos los departamentos.

Puedes probarlos con `curl` o cualquier cliente HTTP. Si quieres ampliar la API, crea nuevas vistas en `projects/api.py` y registra las rutas en `projects/urls.py`.

---

Si encuentras algún problema o deseas contribuir, abre un _issue_ o envía un _pull request_.





