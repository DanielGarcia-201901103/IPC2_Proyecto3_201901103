from flask import Flask,request, jsonify,Response
import xml.etree.ElementTree as et
import xml.etree.cElementTree as ET
import os
import re
from subprocess import check_output
from solicitudUno import Perfil
from solicitudDos import Mensaje

#LISTAS PARA PERFILES
palabrasDescartadas = []
listPerfiles = []
#LISTAS PARA MENSAJES
listMensajes = []

app = Flask(__name__)
app.config['DEBUG'] = True
#print("Iniciando el servidor con el puerto por defecto 5000")

@app.route("/")
def inicio():
    return '<p>Hola, Bienvenido a ChapinChat</p>'

#CARGANDO DATOS PARA LA SOLICITUD UNO correspondiente a perfiles
@app.route("/cargarSolicitudUno",methods=['POST'])
def cargaPerfiles():
    global palabrasDescartadas
    global listPerfiles
    contadorNuevos = 0
    contadorExistentes = 0
    contadorDescartadas = 0
    try:
        archivo = request.data.decode('utf-8')
        raiz = et.XML(archivo)
        for dat in raiz:
            if dat.tag == "perfiles":
                for perf in dat:
                        if perf.tag == "perfil":
                            for dat1 in perf:
                                if dat1.tag == "nombre":
                                    name  = dat1.text
                                elif dat1.tag == "palabrasClave":
                                    #Aqui se lee la lista de palabras
                                    palabrasClave = []
                                    for pal in dat1:
                                        if pal.tag == "palabra":
                                            palabraPerfil = pal.text
                                        palabrasClave.append(str(palabraPerfil).strip())
                            #Si la lista está vacia, ingresa datos
                            if len(listPerfiles) == 0:  
                                objPerfil = Perfil(str(name).strip(),palabrasClave)
                                listPerfiles.append(objPerfil)
                                contadorNuevos += 1
                            elif len(listPerfiles) != 0:          
                            #Recorriendo lista de perfiles
                                boolValidacion = False
                                for i in listPerfiles:
                                    #comparando si el nombre del perfil ya existe
                                    if i.getNombre().lower().strip() == str(name).lower().strip():
                                        #si el nombre existe entonces compara si en la lista de palabras se repite algun dato, sino lo agrega
                                        
                                        for h in palabrasClave:
                                            aux = i.listaPalabrasClave
                                            aux.append(h)
                                            i.listaPalabrasClave = aux
                                        boolValidacion = False
                                        contadorExistentes += 1
                                        break
                                    # Si el nombre del perfil no existe, se agrega a la lista de perfiles el nuevo perfil
                                    elif i.getNombre().lower().strip() != str(name).lower().strip():
                                        boolValidacion = True
                                if boolValidacion == True:
                                    objPerfil = Perfil(str(name).strip(),palabrasClave)
                                    listPerfiles.append(objPerfil) 
                                    contadorNuevos += 1
                                    #print(str(name))
            elif dat.tag == "descartadas":
                for des in dat:
                    if des.tag == 'palabra':
                        palabra_descartada = des.text
                        if len(palabrasDescartadas) == 0:
                            palabrasDescartadas.append(str(palabra_descartada).strip())
                            contadorDescartadas += 1
                        elif len(palabrasDescartadas) != 0:
                            if palabra_descartada in palabrasDescartadas:
                                pass
                            else:
                                palabrasDescartadas.append(str(palabra_descartada).strip())
                                contadorDescartadas += 1
                        
        cadenaNuevos = 'Se han creado '+ str(contadorNuevos)+ ' perfiles nuevos'
        cadenaExistentes = 'Se han actualizado '+str(contadorExistentes)+' perfiles existentes'
        cadenaDescartar = 'Se han creado '+str(contadorDescartadas)+' nuevas palabras a descartar'

        #ESCRIBIENDO ARCHIVO CON RESPUESTAS
        root = ET.Element('respuesta')
        ET.SubElement(root,'perfilesNuevos').text= str(cadenaNuevos)
        ET.SubElement(root,'perfilesExistentes').text= str(cadenaExistentes)
        ET.SubElement(root,'descartadas').text= str(cadenaDescartar)
        ET.indent(root)
        archivo_Respuesta1XML = ET.ElementTree(root)
        archivo_Respuesta1XML.write('ArchivosPrueba\Solicitud1Respuesta'+'.xml')

        leerRespuestaUno = open('ArchivosPrueba\Solicitud1Respuesta.xml','r')
        almacenarRespuesta = '<?xml version="1.0"?>\n'
        almacenarRespuesta += leerRespuestaUno.read()
        leerRespuestaUno.close()

        '''
        print('Palabras Descartadas')
        print(len(palabrasDescartadas))
        for j in palabrasDescartadas:
            print(j)
        print('\nPerfiles')
        print(len(listPerfiles))
        for i in listPerfiles:
            print('\n'+i.getNombre())
            for k in i.listaPalabrasClave:
                print(k)
        '''
        return almacenarRespuesta
    except:
        return jsonify({"message": "Ha ocurrido un error en los datos del archivo xml"})

#CARGANDO DATOS PARA LA SOLICITUD DOS correspondiente a mensajes  
@app.route("/cargarSolicitudDos",methods=['POST'])
def cargarMensajes():
    global listMensajes
    try:
        archivo = request.data.decode('utf-8')
        raiz = et.XML(archivo)
        for dat in raiz:
            if dat.tag == "mensaje":
                mensaje_TextoCompleto  = dat.text
                #print(mensaje_TextoCompleto)
                dato = re.compile('Lugar\s+y\s+Fecha\s*\:\s*(\w+)(\s*|\s*\w+)*(,\s*)(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\/)(0[1-9]|1[0-2])(\/)(\d{4})\s+(0[0-9]|1[0-9]|2[0-3])(:)([0-5][0-9])')
                result = dato.finditer(str(mensaje_TextoCompleto))
                lugFech = ''
                for res in result:
                    #print(inicio,fin)
                    lugFech = res.group()

                dato1 = re.compile(' Usuario\s*:\s*(([a-zA-Z-0-9._-]+@[a-zA-Z-0-9._-]+)|([a-zA-Z-0-9._-]+))')
                result1 = dato1.finditer(str(mensaje_TextoCompleto))
                usua = ''
                for res1 in result1:
                    #print(inicio,fin)
                    usua = res1.group()

                dato3 = re.compile('Red\s+social\s*:\s*(ChapinChat)')
                result3 = dato3.finditer(str(mensaje_TextoCompleto))
                redS = ''
                for res3 in result3:
                    #print(inicio,fin)
                    redS = res3.group()
                '''fechaL = ''
                contador = 0
                while contador < len(result):
                    fechaL += str(result[contador] )
                    contador +=1'''

                print(lugFech)
                print(usua)
                print(redS)
                '''
                EXPRESION PARA LUGAR Y FECHA
Lugar\s+y\s+Fecha\s*\:\s*(\w+)(\s*|\s*\w+)*(,\s*)(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\/)(0[1-9]|1[0-2])(\/)(\d{4})\s+(0[0-9]|1[0-9]|2[0-3])(:)([0-5][0-9])
                EXPRESION PARA USUARIO
                Usuario\s*:\s*(([a-zA-Z-0-9._-]+@[a-zA-Z-0-9._-]+)|([a-zA-Z-0-9._-]+))

                EXPRESION PARA RED
                Red\s+social\s*:\s*(ChapinChat)
                '''
        return 'Leído correctamente'
    except:
        return jsonify({"message": "Ha ocurrido un error en los datos del archivo xml"})


#Ejemplo
#http://localhost:5000/UsuarioConectado?nombreUser=Oscar Leon
@app.route("/ConsultarDatos",methods=['GET'])
def consultarDatos():
    nombreUser = request.args.get('nombreUser')
    print(str(nombreUser))
    return jsonify({"Nombre":nombreUser})  

@app.route("/consultarXfecha",methods=['GET'])
def consultarXFecha():
    nombreUser = request.args.get('nombreUser')
    print(str(nombreUser))
    return jsonify({"Nombre":nombreUser}) 

@app.route("/recibirMensaje",methods=['GET'])
def recibirMensaje():
    texto = request.args.get("asdf")
    return texto

if __name__=='_main_':
    app.run()
#https://github.com/Teitan67/IPC2_EJEMPLO_PY3/blob/main/backend/main.py


#flask --app hello run
#Flask --app Backend\app.py run