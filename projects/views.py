from django.shortcuts import render, hhtpResponse, redirect
from forms.forms import LoginForm, RegisterForm
import requests


# Create your views here.

def post_api_register (post_data):
    
    URL_API = "http://127.0.0.1:8000/api/persona/"
    try:
        post = requests.post(URL_API, json=post_data)
        if post.status_code == 201:
            return post.json()
        else:
            return {"error": f"Error al realizar la solicitud: {post.status_code}", "detalles": post.text}
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"error": "Error de conexión con la API", "details": str(e)}
    
    



