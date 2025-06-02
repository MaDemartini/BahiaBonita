import requests
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from .models import Cliente, Departamento, Reserva, Persona  
from .forms import LoginForm, RegisterForm, AddDeptoForm, ReservaForm
from django.shortcuts import render, HttpResponse, redirect,  get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required



# Create your views here.



########################################################################
#pago transbank API
@login_required
def iniciar_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    valor_total = reserva.valor_total

    url = f"{settings.TRANSBANK_API_URL}/rswebpaytransaction/api/webpay/v1.2/transactions"

    headers = {
        "Tbk-Api-Key-Id": settings.TRANSBANK_COMMERCE_CODE,
        "Tbk-Api-Key-Secret": settings.TRANSBANK_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "buy_order": f"orden_{reserva.id_reserva}",
        "session_id": f"session_{request.session.session_key}",
        "amount": valor_total,
        "return_url": request.build_absolute_uri("/transbank/retorno/")
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        r = response.json()
        return JsonResponse({
            "url_pago": r['url'],
            "token_ws": r['token']
        })
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
            post_data = form.cleaned_data
            post_data['password'] = make_password(form.cleaned_data['password'])
            post_data.pop('re_password')
            response = postApiRegister(post_data)
            if "Datos guardados exitosamente" in response:
                messages.success(request, "Registro exitoso")
                return redirect('login')
            else:
                return render(request, 'register.html', {'form': form, 'error': response.get('error')})
    else:
        form = RegisterForm()
        print("Campos del formulario:", form.fields)
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
# Páginas generales

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
    cant_dormitorios = request.GET.get('cant_dormitorios')  # '1', '2', '3'
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

#########################################################################
# Obtener Cliente de sesión

# Función para obtener Cliente según usuario 
def get_cliente_from_session(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return None
    email = usuario.get('email')
    try:
        return Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return None
    
@login_required
def crear_reserva(request):
    cliente = get_cliente_from_session(request)
    if not cliente:
        messages.error(request, "Debe iniciar sesión para reservar.")
        return redirect('login')

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.id_cliente = cliente

            # Calcular valor total
            depto = reserva.id_departamento
            dias = (reserva.fecha_salida - reserva.fecha_ingreso).days

            # Cálculo aseo según cantidad de habitaciones
            cant_hab = depto.cant_dormitorios
            if cant_hab == 1:
                valor_aseo = 15000
            elif cant_hab == 2:
                valor_aseo = 20000
            elif cant_hab >= 3:
                valor_aseo = 25000
            else:
                valor_aseo = 15000  # fallback

            valor_total = (depto.valor_dia * dias) + valor_aseo
            reserva.valor_total = valor_total
            reserva.tipo_reserva = "diaria"  # Fijo para la web
            reserva.fecha_reserva = date.today()

            # Guardar reserva
            reserva.save()
            messages.success(request, f"Reserva creada con éxito. Total: ${valor_total}")

            # Redirigir a iniciar pago con id reserva
            return redirect('iniciar_pago', reserva_id=reserva.id_reserva)
    else:
        form = ReservaForm(initial={
            'nombre_cliente': cliente.nombre,
            'apellido_clinete': cliente.apellido,
        })
    
    context = {
        'form': form,
        'cliente': cliente,
    }

    return render(request, 'crear_reserva.html', context)



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
                return redirect('index')  
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


def contacto(request):
    return render(request, 'contacto.html')

def estadisticas(request):
    return render(request, 'estadisticas.html')