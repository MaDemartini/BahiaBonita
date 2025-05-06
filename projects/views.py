from django.shortcuts import render, HttpResponse, redirect
import requests
from .forms import Persona, RegisterForm


# Create your views here.

##formulario registro##

def registerPage(request):
    return render(request, 'register.html')

def formsRegister (request):
    form = RegisterForm()
    return render (request, 'register.html', {form:form})



def postApiRegister (post_data):
    
    URL_API = "http://127.0.0.1:8000/api/persona/"
    try:
        post = requests.post(URL_API, json=post_data)
        if post.status_code == 201:
            return {"Datos guardados exitosamente"}
            
        else:
            return {"error": f"Error al realizar la solicitud: {post.status_code}", "detalles": post.text}
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"error": "Error de conexión con la API", "details": str(e)}
    
    



