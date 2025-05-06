from datetime import date
from django.shortcuts import render, HttpResponse, redirect
import requests
from .forms import Persona, RegisterForm


# Create your views here.

##formulario registro##

def registerPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            post_data = form.cleaned_data  # Obtén los datos validados del formulario
            response = postApiRegister(post_data)  # Llama a la función para enviar los datos a la API
            if "Datos guardados exitosamente" in response:
                return redirect('success_page')  # Redirige a una página de éxito
            else:
                return render(request, 'register.html', {'form': form, 'error': response.get('error')})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



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
    
    



