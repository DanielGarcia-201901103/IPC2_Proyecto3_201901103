from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
# Create your views here.

def index(request):
    title = 'Django Course!!'
    return render(request,'index.html',{
        'title': title
    })

def hello(request):
    username = ['a', 'b','c','d', 'e',False,'f']
    return render(request, 'hello.html',{
        'username': username
    })

def help(request):
    headers = {'Content-Type': 'application/xml'}
    response = requests.get('http://127.0.0.1:5000/consultaEstudiante', headers = headers)
    
    diccionario = response.json()
    #listProgramador = diccionario.values()
    #listProgramador = list(listProgramador)
    print(diccionario)
    return render(request, 'help.html',{'diccionario': diccionario})

'''
def help(request):
    return HttpResponse("<h1>Acerca de</h1>")

'''

