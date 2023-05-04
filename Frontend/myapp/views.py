from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
# Create your views here.

def index(request):
    title = 'Bienvenido a ChapinChat!'
    return render(request,'index.html',{
        'title': title
    })

def servicio(request):
    username = ['a', 'b','c','d', 'e',False,'f']
    return render(request, 'solicitarServicio.html',{
        'username': username
    })

def peticiones(request):
    username = ['a', 'b','c','d', 'e',False,'f']
    return render(request, 'peticiones.html',{
        'username': username
    })

def limpiar(request):
    response = requests.delete('http://127.0.0.1:5000/resetDatos')
    return render(request, 'limpiar.html')

def help(request):
    headers = {'Content-Type': 'application/xml'}
    response = requests.get('http://127.0.0.1:5000/consultaEstudiante', headers = headers)
    
    diccionario = response.json()
    nombre = diccionario["Nombre"]
    carne = diccionario["Carne"]
    #convirtiendo diccionario a lista a partir de los valores
    #diccionario = diccionario.values()
    #diccionario = list(diccionario)
    mensaje = ''
    if request.method == 'GET':
        response1 = requests.get('http://127.0.0.1:5000/visualizandoDocumentacion',headers = headers)
        mensaje = response1.text
        #print(mensaje)
    return render(request, 'help.html',{'nombre': nombre, 'carne': carne, "respuesta_servidor": mensaje})

'''
def help(request):
    return HttpResponse("<h1>Acerca de</h1>")

'''

