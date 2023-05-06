from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
import xml.etree.ElementTree as ET
# Create your views here.

def index(request):
    title = 'Bienvenido a ChapinChat!'
    return render(request,'index.html',{
        'title': title
    })

def servicioUno(request):
    if request.method == 'POST':
        archivo = request.FILES['mensaje']
        headers = {'Content-Type': 'application/xml'}
        response = requests.post('http://127.0.0.1:5000/cargarSolicitudUno', data=archivo.read(), headers=headers)

        if response.status_code==200:
            print("Correcto")
            datosxml = response.text
            #parsed_xml = ET.fromstring(datosxml)
            #sorted_xml = ET.ElementTree(parsed_xml)
            #sorted_xml.write('sorted_xml.xml', encoding='utf-8', xml_declaration= True)
            #with open('sorted_xml.xml', 'r') as file:
            #    sorted_xml_data = file.read()
            respuesta_servidor = datosxml

            return render(request, 'solicitarUno.html',{'respuesta_servidor':respuesta_servidor})
        else:
            print("incorrecto")
            return render(request, 'solicitarUno.html',{'respuesta_servidor':'Incorrecto'})    
    else:
        return render(request, 'solicitarUno.html',{'respuesta_servidor':''})
#Enlace para resolver algunos errores    
#https://sydjameer.medium.com/how-to-resolve-forbidden-403-if-django-csrf-mechanism-has-not-been-used-in-post-method-1aeeb8540404

def servicioDos(request):
    if request.method == 'POST':
        archivo = request.FILES['mensaje']
        headers = {'Content-Type': 'application/xml'}
        response = requests.post('http://127.0.0.1:5000/cargarSolicitudDos', data=archivo.read(), headers=headers)

        if response.status_code==200:
            print("Correcto")
            datosxml = response.text
            #parsed_xml = ET.fromstring(datosxml)
            #sorted_xml = ET.ElementTree(parsed_xml)
            #sorted_xml.write('sorted_xml.xml', encoding='utf-8', xml_declaration= True)
            #with open('sorted_xml.xml', 'r') as file:
            #    sorted_xml_data = file.read()
            respuesta_servidor = datosxml

            return render(request, 'solicitarDos.html',{'respuesta_servidor':respuesta_servidor})
        else:
            print("incorrecto")
            return render(request, 'solicitarDos.html',{'respuesta_servidor':'Incorrecto'})    
    else:
        return render(request, 'solicitarDos.html',{'respuesta_servidor':''})

def detalleMensajes(request):
    if request.method == 'POST':
        fecha_Obtenida = request.POST.get('fecha')
        usuario_Obtenido = request.POST.get('usuario')
        xml = f"<busqueda><fecha>{fecha_Obtenida}</fecha><usuario>{usuario_Obtenido}</usuario></busqueda>"
        
        headers = {'Content-Type': 'application/xml'}
        response = requests.post('http://127.0.0.1:5000/detalleMensajesporUsuario', data=xml, headers=headers)

        if response.status_code==200:
            print("Correcto")
            datosxml = response.json()

            #parsed_xml = ET.fromstring(datosxml)
            #sorted_xml = ET.ElementTree(parsed_xml)
            #sorted_xml.write('sorted_xml.xml', encoding='utf-8', xml_declaration= True)
            #with open('sorted_xml.xml', 'r') as file:
            #    sorted_xml_data = file.read()
            respuesta_servidor = datosxml['lista']

            return render(request, 'detalleMensajess.html',{'respuesta_servidor':'Tabla realizada'})
        else:
            print("incorrecto")
            return render(request, 'detalleMensajess.html',{'respuesta_servidor':'Incorrecto'})    
    else:
        return render(request, 'detalleMensajess.html',{'respuesta_servidor':''})

def resumenPesos(request):
    pass

def creacion1Mensaje(request):
    if request.method == 'POST':
        archivo = request.FILES['mensaje']
        headers = {'Content-Type': 'application/xml'}
        response = requests.post('http://127.0.0.1:5000/peticionCreacionMensajes', data=archivo.read(), headers=headers)

        if response.status_code==200:
            print("Correcto")
            datosxml = response.text
            #parsed_xml = ET.fromstring(datosxml)
            #sorted_xml = ET.ElementTree(parsed_xml)
            #sorted_xml.write('sorted_xml.xml', encoding='utf-8', xml_declaration= True)
            #with open('sorted_xml.xml', 'r') as file:
            #    sorted_xml_data = file.read()
            respuesta_servidor = datosxml

            return render(request, 'creacionUnMensaje.html',{'respuesta_servidor':respuesta_servidor})
        else:
            print("incorrecto")
            return render(request, 'creacionUnMensaje.html',{'respuesta_servidor':'Incorrecto'})    
    else:
        return render(request, 'creacionUnMensaje.html',{'respuesta_servidor':''})

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
'''
def peticiones(request):
    username = ['a', 'b','c','d', 'e',False,'f']
    return render(request, 'peticiones.html',{
        'username': username
    })
'''
