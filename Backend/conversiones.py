import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import re
from io import BytesIO
validaDatos = {
    'Deportista':['fútbol', 'balonmano', 'baloncesto', 'balompié', 'football', 'basketball', 'handball', 'estadio', 'selección', 'champions league', 'liga de campeones', 'tenis', 'natación', 'olimpiada', 'gym', 'gimnasio'],

    'CulturaSaludable':['gimnasio', 'comida saludable', 'ejercicio', 'maratón', 'carrera', 'entreno', 'entrenar', 'entrenamiento', 'pesas', 'karate', 'tae kwon do', 'boxeo', 'gym', 'healthy food', 'vitaminas', 'caminata', 'caminar', 'ropa deportiva', 'bebida hidratante', 'bebidas hidratantes'],

    'Excluidas':['a', 'un', 'una', 'en', 'para', 'por', 'que', 'qué', 'la', 'las', 'los', 'el', 'unas', 'si', 'no', 'sino', 'entre', 'otro', 'otra', 'otros', 'otras', 'de', 'del', 'nos', 'sus', 'su', 'am', 'pm']

}

def pXmL(xml):
    if xml:
        doc=ET.fromstring(xml)
        artista=doc.find('artista')
        cancion=doc.find('cancion')
        lirica=doc.find('letra')
        palabras=ObtenerListadePalabras(lirica.text)

        return ObtenerProcentajesDeGeneros(palabras,artista.text,cancion.text)

def ObtenerListadePalabras(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\b\d+\b', '', text)
    words = text.lower().split()
    words =EliminarPalabras(words)
    return words


def EliminarPalabras(lista):
    Listaeliminar=validaDatos['Excluidas']
    for palabra in lista:
        if palabra.lower() in [eliminar.lower() for eliminar in Listaeliminar]:
            lista.remove(palabra)
    return lista

def ObtenerProcentajesDeGeneros(listaPalabras,artista,cancion):
    totalPalabras=len(listaPalabras)
    root=Element('respuesta')
    SubElement(root,'artista').text=artista
    SubElement(root,'nombre').text=cancion
    SubElement(root,'totalpalabras').text=str(totalPalabras)
    categorias=SubElement(root,'categorias')
    
def ObtenerProcentajesDeGeneros(listaPalabras,artista,cancion):
    totalPalabras=len(listaPalabras)
    root=Element('respuesta')
    SubElement(root,'artista').text=artista
    SubElement(root,'nombre').text=cancion
    SubElement(root,'totalpalabras').text=str(totalPalabras)
    categorias=SubElement(root,'categorias')
    
    
    coincidencias=0
    for genero, palabrasgenero in validaDatos.items():
        if genero!='Eliminar':
            coincidencias=0
            for palabra in listaPalabras:
                if palabra.lower() in [p.lower() for p in palabrasgenero]:
                    coincidencias+=1
            categoria=SubElement(categorias,'categoria')
            SubElement(categoria,'nombre').text=genero
            SubElement(categoria,'coincidencias').text=str(coincidencias)
            SubElement(categoria,'porcentaje').text=str((coincidencias/totalPalabras)*100)
    tree = ElementTree(root)
    xml_data = BytesIO()
    xml_bytes = tree.write(xml_data,encoding='UTF-8', xml_declaration=True)
    return xml_data.getvalue()
