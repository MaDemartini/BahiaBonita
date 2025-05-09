from datetime import date
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import requests
from .forms import Persona, RegisterForm
from django.conf import settings


# Create your views here.

##formulario registro##

########################################################################

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
    
#########################################################################


#########################################################################
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



##################################################################
def postApiRegister (post_data):
    
    URL_API = "http://127.0.0.1:8000/api/persona/"

     # Convertir fecha_nacimiento a string si es tipo date
    if isinstance(post_data.get("fecha_nacimiento"), date):
        post_data["fecha_nacimiento"] = post_data["fecha_nacimiento"].isoformat()
    try:
        print(f"Enviando datos a la API: {post_data}")
        post = requests.post(URL_API, json=post_data)
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



