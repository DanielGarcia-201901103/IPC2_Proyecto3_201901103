from flask import Flask,request, jsonify,Response
import xml.etree.ElementTree as et
import os
from subprocess import check_output
from solicitudUno import Perfil

palabrasDescartadas = []
listPerfiles = []

app = Flask(__name__)
app.config['DEBUG'] = True
#print("Iniciando el servidor con el puerto por defecto 5000")

@app.route("/")
def inicio():
    return '<p>Hola, Bienvenido a ChapinChat</p>'

#CARGANDO DATOS PARA LA SOLICITUD UNO
@app.route("/cargarSolicitudUno",methods=['POST'])
def ObtenerDatos():
    global palabrasDescartadas
    global listPerfiles
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
                            else:          
                            #Recorriendo lista de perfiles
                                boolValidacion = False
                                for i in listPerfiles:
                                    #comparando si el nombre del perfil ya existe
                                    if i.getNombre().lower() == str(name).lower().strip():
                                        #si el nombre existe entonces compara si en la lista de palabras se repite algun dato, sino lo agrega
                                        for k in i.listaPalabrasClave:
                                            for h in palabrasClave:
                                                if k.lower() != h.lower():
                                                    i.listaPalabrasClave.append(h)
                                        boolValidacion = False
                                        break
                                    # Si el nombre del perfil no existe, se agrega a la lista de perfiles el nuevo perfil
                                    elif i.getNombre().lower() != str(name).lower().strip():
                                        boolValidacion = True
                                if boolValidacion == True:
                                    objPerfil = Perfil(str(name).strip(),palabrasClave)
                                    listPerfiles.append(objPerfil) 
            elif dat.tag == "descartadas":
                for des in dat:
                    if des.tag == 'palabra':
                        palabra_descartada = des.text
                    if len(palabrasDescartadas) == 0:
                        palabrasDescartadas.append(str(palabra_descartada).strip())
                    else:
                        if palabra_descartada in palabrasDescartadas:
                            pass
                        else:
                            palabrasDescartadas.append(str(palabra_descartada).strip())
                        

        '''
        print('Palabras Descartadas')
        for j in palabrasDescartadas:
            print(j)
        print('Perfiles')
        for i in listPerfiles:
            print(i.getNombre())
            for k in i.listaPalabrasClave:
                print(k)'''
        return jsonify({'message':'Archivo leído correctamente',})
    except:
        return jsonify({"message": "Ha ocurrido un error"})
    
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