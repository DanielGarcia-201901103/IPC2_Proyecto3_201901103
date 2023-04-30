from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests

def Song(request):
    if request.method == 'POST':
        # Procesar el formulario cuando se envíe
        nombre_artista = request.POST.get('artista')
        nombre_cancion = request.POST.get('cancion')
        letra_cancion = request.POST.get('letras')
        xml = f"<mensaje><artista>{nombre_artista}</artista><cancion>{nombre_cancion}</cancion><letra>{letra_cancion}</letra></mensaje>"

        
        headers = {'Content-Type': 'application/xml'}
        response = requests.post('http://127.0.0.1:5000/procesarSolicitud', data=xml, headers=headers)

        if response.status_code == 201:
            xml_str = response.content.decode('utf-8')
            root = ET.fromstring(xml_str)
            respuesta_servidor="La cancion: "+root.find('nombre').text+'\n Del artista: '+root.find('artista').text+'\n'
            
            categorias=[]
            for cat in root.iter('categoria'):
                temporal={
                    'categoria':cat.find('nombre').text,
                    'coincidencias':cat.find('coincidencias').text,
                    'porcentaje':cat.find('porcentaje').text
                }
                categorias.append(temporal)
            
            return render(request, 'index.html', {'respuesta_servidor': respuesta_servidor,'categorias':categorias})
        else:
            respuesta_servidor = response.text
            return render(request, 'index.html', {'respuesta_servidor': "Sin Canciones"})
    else:
        # Mostrar el formulario vacío en la página
        contexto = {
            'respuesta_servidor': None
        }
        return render(request, 'index.html', contexto)