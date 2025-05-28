import requests
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from .models import Cliente, Departamento, Reserva, Persona  
from .forms import LoginForm, Persona, RegisterForm, AddDeptoForm
from django.shortcuts import render, HttpResponse, redirect,  get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

# Create your views here.



########################################################################
#pago transbank API
def iniciar_pago(request):
    url = f"{settings.TRANSBANK_API_URL}/rswebpaytransaction/api/webpay/v1.2/transactions"

    headers = {
        "Tbk-Api-Key-Id": settings.TRANSBANK_COMMERCE_CODE,
        "Tbk-Api-Key-Secret": settings.TRANSBANK_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "buy_order": "orden123",
        "session_id": "session456",
        "amount": 25000,
        "return_url": request.build_absolute_uri("/transbank/retorno/")
    }

    try:
        # 👇 Este es el correcto
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        r = response.json()
        return redirect(f"{r['url']}?token_ws={r['token']}")
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# Confirmación de pago
# Esta vista se llama desde el Webpay después de que el usuario completa el pago

def confirm_pago(request):
    token = request.GET.get("token_ws")
    
    if not token:
        return JsonResponse({"error": "Token no proporcionado"}, status=422)

    url = f"{settings.TRANSBANK_API_URL}/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"

    headers = {
        "Tbk-Api-Key-Id": settings.TRANSBANK_COMMERCE_CODE,
        "Tbk-Api-Key-Secret": settings.TRANSBANK_API_KEY
    }

    try:
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        datos_pago = response.json()
        return JsonResponse(datos_pago)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
#########################################################################



#########################################################################
#crear registro de usuarios mediante API
def postApiRegister (post_data):
    
    url = settings.URL_API_REGISTRO

     # Convertir fecha_nacimiento a string si es tipo date
    if isinstance(post_data.get("fecha_nacimiento"), date):
        post_data["fecha_nacimiento"] = post_data["fecha_nacimiento"].isoformat()
    try:
        print(f"Enviando datos a la API: {post_data}")
        post = requests.post(url, json=post_data)
        print(f"Respuesta de la API: {post.status_code}, {post.text}")  # Verifica la respuesta de la API
        if post.status_code == 201:
            return {"Datos guardados exitosamente"}
            
        else:
            return {"error": f"Error al realizar la solicitud: {post.status_code}", "detalles": post.text}
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"error": "Error de conexión con la API", "details": str(e)}  

def registerPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            post_data = form.cleaned_data  # Obtén los datos validados del formulario
            response = postApiRegister(post_data)  # Llama a la función para enviar los datos a la API
            if "Datos guardados exitosamente" in response:
                messages.success(request, "Registro exitoso")
                return redirect('registro')  # Redirige a una página de éxito
            else:
                return render(request, 'register.html', {'form': form, 'error': response.get('error')})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form}) 

#########################################################################

def postApiLogin(data):
    url = settings.URL_API_LOGIN 
    try:
        response = requests.post(url, json=data)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con API login: {e}")
        return None

def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password']
            }
            response = postApiLogin(data)
            if response and response.status_code == 200:
                user_data = response.json()

                # Guarda la sesión o token, si lo usas
                request.session['usuario'] = user_data
                messages.success(request, f"¡Bienvenido, {user_data.get('nombre', '')}!")

                return redirect('index')

            else:
                messages.error(request, "Correo o contraseña incorrectos")
    return render(request, 'login.html', {'form': form})

@api_view(['POST'])
def api_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        persona = Persona.objects.get(email=email)
        if check_password(password, persona.password):  # Solo si guardas password hasheado
            return Response({
                "id": persona.id_persona,
                "nombre": persona.nombre,
                "email": persona.email,
                "rol": persona.rol  # o usa una función get_rol(persona)
            }, status=200)
        else:
            return Response({"error": "Contraseña incorrecta"}, status=401)
    except Persona.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

#########################################################################
#crear deptos mediante API
def administracion(request):
    departamentos = []
    clientes = []

    if request.method == 'POST':
        form = AddDeptoForm(request.POST)
        if form.is_valid():
            url = settings.URL_API_ADDDEPTO  # Asegúrate de que esta URL esté definida en tu settings.py
            data = form.cleaned_data
            response = requests.post(url, json=data)
            if response.status_code == 201:
                messages.success(request, "Departamento agregado exitosamente")
                return redirect('administracion')  # Redirige a la misma página para ver el nuevo departamento
            else:
                messages.error(request, f"Error al agregar el departamento: {response.status_code} - {response.text}")
    else:
        form = AddDeptoForm()

    # Obtener departamentos desde la API
    page_obj = []
    try:
        response_depto = requests.get(settings.URL_API_ADDDEPTO) 
        if response_depto.status_code == 200:
            departamentos = response_depto.json()        
            paginator = Paginator(departamentos, 2)  # Muestra la cantidad de departamentos por página
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
    except Exception as e:
        messages.error(request, f"Error al cargar los departamentos: {e}")  
         

   #obtener clientes desde la API
    try:
        response_clientes = requests.get(settings.URL_API_CLIENTE)
        if response_clientes.status_code == 200:
            clientes = response_clientes.json()
    except Exception as e:
        messages.error(request, f"Error al cargar clientes: {e}")

    return render(request, 'administracion.html', {'form': form,'clientes': clientes, 'page_obj' : page_obj})
#eliminar deptos mediante API
def eliminar_depto(request, id):
    url = f"{settings.URL_API_ADDDEPTO}{id}/"  # Asegúrate de que esta URL esté definida en tu settings.py
    response = requests.delete(url)
    if response.status_code == 204: #el codigo 204 indica que la solicitud fue exitosa y no hay contenido para devolver
        messages.success(request, "Departamento eliminado exitosamente")
    else:
        messages.error(request, f"Error al eliminar el departamento: {response.status_code} - {response.text}")
    return redirect('administracion')  # Redirige a la página de administración
        
#########################################################################

def index(request):
    return render(request, 'index.html')

def servicios(request):
    return render(request, 'servicios.html')

def departamentos(request):
    departamentos = []
    try:
        response = requests.get(settings.URL_API_ADDDEPTO)
        if response.status_code == 200:
            departamentos = response.json()
        else:
            messages.error(request, f"Error al obtener departamentos: {response.status_code}")
    except Exception as e:
        messages.error(request, f"Error al conectar con la API de departamentos: {e}")

    # Filtrar departamentos que NO están en mantenimiento (solo disponibles)
    departamentos = [d for d in departamentos if not d.get('mantenimiento', False)]

    # FILTROS desde GET (query params)
    cant_dormitorios = request.GET.get('cant_dormitorios')  # Ej: '1', '2', '3'
    cant_banos = request.GET.get('cant_banos')
    piso = request.GET.get('piso')
    cant_personas = request.GET.get('cant_personas')

    if cant_dormitorios:
        departamentos = [d for d in departamentos if str(d.get('cant_dormitorios', '')) == cant_dormitorios]
    if cant_banos:
        departamentos = [d for d in departamentos if str(d.get('cant_banos', '')) == cant_banos]
    if piso:
        departamentos = [d for d in departamentos if str(d.get('piso', '')) == piso]
    if cant_personas:
        departamentos = [d for d in departamentos if str(d.get('cant_personas', '')) == cant_personas]

    # PAGINACIÓN
    paginator = Paginator(departamentos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filtros': {
            'cant_dormitorios': cant_dormitorios,
            'cant_banos': cant_banos,
            'piso': piso,
            'cant_personas': cant_personas,
        }
    }
    return render(request, 'departamentos.html', context)


def crear_reserva(request, id_departamento=None):
    departamento = None
    error = None

    if id_departamento:
        try:
            response = requests.get(f"{settings.URL_API_ADDDEPTO}{id_departamento}/")
            if response.status_code == 200:
                departamento = response.json()
            else:
                error = f"Error al cargar el departamento. Código: {response.status_code}"
        except Exception as e:
            error = f"Error al conectar con la API: {e}"

    return render(request, 'crear_reserva.html', {
        'departamento': departamento,
        'error': error
    })


def guardar_reserva(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            email = request.POST['email']
            departamento_id = request.POST['departamento']
            fecha_ingreso = parse_date(request.POST['fecha_ingreso'])
            fecha_salida = parse_date(request.POST['fecha_salida'])
            cant_personas = int(request.POST['cant_personas'])
            tipo_reserva = request.POST['tipo_reserva']
            valor_total = float(request.POST['valor_total'])

            # Datos para enviar a la API
            reserva_data = {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "departamento": departamento_id,
                "fecha_ingreso": fecha_ingreso.isoformat(),
                "fecha_salida": fecha_salida.isoformat(),
                "cant_personas": cant_personas,
                "tipo_reserva": tipo_reserva,
                "valor_total": valor_total
            }

            response = requests.post(settings.URL_API_RESERVA, json=reserva_data)

            if response.status_code == 201:
                messages.success(request, "Reserva guardada correctamente.")
                return redirect('index')  # O donde desees redirigir tras reservar
            else:
                messages.error(request, f"Error al guardar la reserva: {response.status_code} - {response.text}")
                return redirect('crear_reserva')

        except Exception as e:
            messages.error(request, f"Error inesperado al guardar la reserva: {str(e)}")
            return redirect('crear_reserva')
    else:
        return HttpResponse("Método no permitido", status=405)


def inicio_pago(request):
    return render(request, 'inicio_pago.html')

def confirm_pago(request):
    return render(request, 'retorno.html')

def contacto(request):
    return render(request, 'contacto.html')

def registerPage(request):
    return render(request, 'register.html')

def loginPage(request):
    return render(request, 'login.html')

def administracion(request):
    return render(request, 'administracion.html')

def estadisticas(request):
    return render(request, 'estadisticas.html')