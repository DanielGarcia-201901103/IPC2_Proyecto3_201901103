from flask import Flask,request, jsonify,Response
import xml.etree.ElementTree as et
import xml.etree.cElementTree as ET
import os
import re
import webbrowser
from subprocess import check_output
from solicitudUno import Perfil
from solicitudDos import Mensaje
import calculos
#LISTAS PARA PERFILES
palabrasDescartadas = []
listPerfiles = []
#LISTAS PARA MENSAJES
listMensajes = []
#Esta lista solo sirve para manejar los datos del metodo cargarMensajes
listAuxUsuarios = []

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
        archivo_Respuesta1XML.write('Backend\ArchivosXML\Solicitud1Respuesta'+'.xml')

        leerRespuestaUno = open('Backend\ArchivosXML\Solicitud1Respuesta.xml','r')
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
        return "Ha ocurrido un error en los datos del archivo xml"

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
                dato = re.compile('(Lugar|LUGAR|lugar)\s+(y|Y)\s+(Fecha|fecha|FECHA)\s*\:\s+(\w+)(\s*|\s*\w+)*(,\s*)(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\/)(0[1-9]|1[0-2])(\/)(\d{4})\s+(0[0-9]|1[0-9]|2[0-3])(:)([0-5][0-9])')
                result = dato.finditer(str(mensaje_TextoCompleto))
                lugFech = ''
                for res in result:
                    #print(inicio,fin)
                    lugFech = res.group()
                lislugFech = lugFech.rsplit(": ")
                #print(lislugFech[1].strip())
                lislugFech1 = lislugFech[1].rsplit(",")
                #print(lislugFech1[0].strip())
                #print(lislugFech1[1].strip())

                dato1 = re.compile('(Usuario|usuario|USUARIO)\s*:\s+(([a-zA-Z-0-9._-]+@[a-zA-Z-0-9._-]+)|([a-zA-Z-0-9._-]+))')
                result1 = dato1.finditer(str(mensaje_TextoCompleto))
                usua = ''
                for res1 in result1:
                    #print(inicio,fin)
                    usua = res1.group()
                liusua = usua.rsplit(": ")

                dato3 = re.compile('(Red|RED|red)\s+(social|SOCIAL|Social)\s*:\s+(ChapinChat)')
                result3 = dato3.finditer(str(mensaje_TextoCompleto))
                redS = ''
                for res3 in result3:
                    #print(inicio,fin)
                    redS = res3.group()
                liredS = redS.rsplit(": ")

                dato4 = re.compile('ChapinChat\s*(\s*[A-Za-z-09]*.*)*')
                result4 = dato4.finditer(str(mensaje_TextoCompleto))
                soloMensaje = ''
                for res4 in result4:
                    soloMensaje = res4.group()
                soloMensaje = soloMensaje.replace("ChapinChat",'')
                '''fechaL = ''
                contador = 0
                while contador < len(result):
                    fechaL += str(result[contador] )
                    contador +=1'''

                #print(lislugFech[1].strip())
                #print(liusua[1].strip())
                #print(liredS[1].strip())
                #print(soloMensaje.strip())
                listaProbabilidadesCalulados = calculos.calcularDatos(listPerfiles,palabrasDescartadas,str(soloMensaje).strip())

                objetoMensaje = Mensaje(str(lislugFech1[0]).strip(),str(lislugFech1[1]).strip(),str(liusua[1]).strip(),str(liredS[1]).strip(),str(soloMensaje).strip(), listaProbabilidadesCalulados)

                listMensajes.append(objetoMensaje)
                listAuxUsuarios.append(str(liusua[1]).strip())
        listaSinRepetidos = list(set(listAuxUsuarios))

        cadenaCantidadUsuariosUnicos = 'Se procesaron mensajes para '+str(len(listaSinRepetidos))+' usuarios distintos'
        cadenaCantidadMensajes = 'Se procesaron '+str(len(listMensajes))+' mensajes en total'

        #ESCRIBIENDO ARCHIVO CON RESPUESTAS
        root1 = ET.Element('respuesta')
        ET.SubElement(root1,'usuarios').text= str(cadenaCantidadUsuariosUnicos)
        ET.SubElement(root1,'mensajes').text= str(cadenaCantidadMensajes)
        ET.indent(root1)
        archivo_Respuesta2XML = ET.ElementTree(root1)
        archivo_Respuesta2XML.write('Backend\ArchivosXML\Solicitud2Respuesta'+'.xml')

        leerRespuestaDos = open('Backend\ArchivosXML\Solicitud2Respuesta.xml','r')
        almacenarRespuesta1 = '<?xml version="1.0"?>\n'
        almacenarRespuesta1 += leerRespuestaDos.read()
        leerRespuestaDos.close()

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

        '''
                EXPRESION PARA LUGAR Y FECHA
Lugar\s+y\s+Fecha\s*\:\s*(\w+)(\s*|\s*\w+)*(,\s*)(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\/)(0[1-9]|1[0-2])(\/)(\d{4})\s+(0[0-9]|1[0-9]|2[0-3])(:)([0-5][0-9])
                EXPRESION PARA USUARIO
                Usuario\s*:\s*(([a-zA-Z-0-9._-]+@[a-zA-Z-0-9._-]+)|([a-zA-Z-0-9._-]+))

                EXPRESION PARA RED
                Red\s+social\s*:\s*(ChapinChat)

                EXPRESION REGULAR PARA MENSAJE
                ChapinChat\s*(\s*[A-Za-z-09]*.*)*
        '''
        return almacenarRespuesta1
    except:
        return "Ha ocurrido un error en los datos del archivo xml"

#Metodo para inicializar la aplicación, dejarla sin datos
@app.route("/resetDatos",methods=['DELETE'])
def inicializarDatos():
    try:
        global palabrasDescartadas
        global listPerfiles
        global listMensajes
        global listAuxUsuarios
        palabrasDescartadas = []
        listPerfiles = []
        listMensajes = []
        listAuxUsuarios = []
        return jsonify({"message": "Ha regresado al estado inicial"})
    except:
        return jsonify({"message": "Ha ocurrido un error en reset"})

#Metodo para consultar datos del programador
@app.route("/consultaEstudiante",methods=['GET'])
def consultarDatosProgramador():
    try:
        datosEstudiante = 'Josué Daniel Rojché García'
        datosCarne = '201901103'
        #jsonify({"Nombre":datosEstudiante, "Carne": datosCarne}) 
        return jsonify({"Nombre":datosEstudiante, "Carne": datosCarne}) 
    except:
        return jsonify({"message": "Ha ocurrido un error en datos programador"})
    
#Metodo para consultar la documentación
@app.route("/visualizandoDocumentacion",methods=['GET'])
def visualDocumentacion():
    try:
        #ArchivosPrueba\Solicitud1Respuesta.xml
        pathTecnico = "Documentacion\documentacion.pdf" 
        webbrowser.open_new(pathTecnico)
    
        return "documentacion mostrada"
    except:
        return "Ha ocurrido un error en consulta documentacion"
#Los metodos anteriores ya funcionan
#CARGANDO DATOS PARA PETICIONES Prueba  de  solicitudes  de  creación  de  mensajes, falta manejar perfiles para calculos
@app.route("/peticionCreacionMensajes",methods=['POST'])
def solicitudesCreacionMensajes():
    global listMensajes
    try:
        archivo = request.data.decode('utf-8')
        raiz = et.XML(archivo)
        #for dat in raiz:
        if raiz.tag == "mensaje":
            mensaje_TextoCompleto  = raiz.text
            #print(mensaje_TextoCompleto)
            dato = re.compile('(Lugar|LUGAR|lugar)\s+(y|Y)\s+(Fecha|fecha|FECHA)\s*\:\s+(\w+)(\s*|\s*\w+)*(,\s*)(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\/)(0[1-9]|1[0-2])(\/)(\d{4})\s+(0[0-9]|1[0-9]|2[0-3])(:)([0-5][0-9])')
            result = dato.finditer(str(mensaje_TextoCompleto))
            lugFech = ''
            for res in result:
                #print(inicio,fin)
                lugFech = res.group()
            lislugFech = lugFech.rsplit(": ")
            #print(lislugFech[1].strip())
            lislugFech1 = lislugFech[1].rsplit(",")
            #print(lislugFech1[0].strip())
            #print(lislugFech1[1].strip())

            dato1 = re.compile('(Usuario|usuario|USUARIO)\s*:\s+(([a-zA-Z-0-9._-]+@[a-zA-Z-0-9._-]+)|([a-zA-Z-0-9._-]+))')
            result1 = dato1.finditer(str(mensaje_TextoCompleto))
            usua = ''
            for res1 in result1:
                #print(inicio,fin)
                usua = res1.group()
            liusua = usua.rsplit(": ")

            dato3 = re.compile('(Red|RED|red)\s+(social|SOCIAL|Social)\s*:\s+(ChapinChat)')
            result3 = dato3.finditer(str(mensaje_TextoCompleto))
            redS = ''
            for res3 in result3:
                #print(inicio,fin)
                redS = res3.group()
            liredS = redS.rsplit(": ")

            dato4 = re.compile('ChapinChat\s*(\s*[A-Za-z-09]*.*)*')
            result4 = dato4.finditer(str(mensaje_TextoCompleto))
            soloMensaje = ''
            for res4 in result4:
                soloMensaje = res4.group()
            soloMensaje = soloMensaje.replace("ChapinChat",'')
            #print(lislugFech[1].strip())
            #print(liusua[1].strip())
            #print(liredS[1].strip())
            #print(soloMensaje.strip())

            listaProbabilidadesCalulados = calculos.calcularDatos(listPerfiles,palabrasDescartadas,str(soloMensaje).strip())

            objetoMensaje = Mensaje(str(lislugFech1[0]).strip(),str(lislugFech1[1]).strip(),str(liusua[1]).strip(),str(liredS[1]).strip(),str(soloMensaje).strip(), listaProbabilidadesCalulados)

            listMensajes.append(objetoMensaje)

            #listaPesosCalculados = calculos.calcularPeso(listMensajes, str(liusua[1]).strip())

        '''
        <?xml version="1.0"?> 
        <respuesta> 
            <fechaHora> 01/04/2023 15:21 </fechaHora>  
            <usuario> map0002@usac.edu </usuario> 
            <perfiles> 
                <perfil nombre=Deportista> 
                    <porcentajeProbabilidad> 10.71% </porcentajeProbabilidad> 
                    <pesoActual> 11.22 </pesoActual> 
                </perfil> 
                ...  
            </perfiles> 
        </respuesta> 
        
        '''
        #ESCRIBIENDO ARCHIVO CON RESPUESTAS
        root1 = ET.Element('respuesta')
        ET.SubElement(root1,'fechaHora').text= str(lislugFech1[1]).strip()
        ET.SubElement(root1,'usuario').text= str(liusua[1]).strip()
        perfs = ET.SubElement(root1,'perfiles')
        
        for j in listaProbabilidadesCalulados:
            auxiliarPerfil = j.perfil
            auxiliarPorcentaje = j.porcentaje
            perf = ET.SubElement(perfs,'perfil', nombre = str(auxiliarPerfil))
            ET.SubElement(perf,'porcentajeProbabilidad').text= str(str(auxiliarPorcentaje)+' %')


        ET.indent(root1)
        archivo_Respuesta2XML = ET.ElementTree(root1)
        archivo_Respuesta2XML.write('Backend\ArchivosXML\peticionSolicitudCMensajes'+'.xml')

        leerRespuestaDos = open('Backend\ArchivosXML\peticionSolicitudCMensajes.xml','r')
        almacenarRespuesta1 = '<?xml version="1.0"?>\n'
        almacenarRespuesta1 += leerRespuestaDos.read()
        leerRespuestaDos.close()
        
        return almacenarRespuesta1
    except:
        return "Ha ocurrido un error en los datos del archivo xml"

@app.route("/resumenPesosporUsuario",methods=['GET'])
def pesosPorUsuario():
    try:
        pass
        return jsonify({"message":'falta realizar los calculos'}) 
    except:
        return jsonify({"message": "Ha ocurrido un error"})

@app.route("/detalleMensajesporUsuario",methods=['POST'])
def detalleMensajesPorUsuario():
    global listMensajes
    try:
        #<busqueda><fecha>{fecha_Obtenida}</fecha><usuario>{usuario_Obtenido}</usuario></busqueda>
        #Obtener la fecha por la cual se va buscar
        archivo = request.data.decode('utf-8')
        raiz = et.XML(archivo)
        for dat in raiz:
            if dat.tag == "fecha":
                busqueda_fecha  = dat.text
            elif dat.tag == "usuario":
                busqueda_usuario  = dat.text
        #print(busqueda_fecha)
        #print(busqueda_usuario)
        #validar si la busqueda será por un usuario especifico o por medio de todos
        #buscar por la fecha
        listaEncontrados = []
        
        if busqueda_usuario.lower().strip() == 'todos':
            for todosUsuarios in listMensajes:
                #Obteniendo fecha de la lista
                almacenadaFecha = todosUsuarios.fechaHora
                if busqueda_fecha.lower().strip() in almacenadaFecha.lower().strip():
                    print("fecha encontrada"+ busqueda_fecha)
                    listaEncontrados.append(todosUsuarios)

        else:
            for usuarios1 in listMensajes:
                #Obteniendo fecha de la lista
                almacenadaFecha = usuarios1.fechaHora
                almacenadaUsuario = usuarios1.usuario
                if busqueda_fecha.lower().strip() in almacenadaFecha.lower().strip():
                    if busqueda_usuario.lower().strip() == almacenadaUsuario.lower().strip():
                        print("Usuario unico encontrado"+ busqueda_usuario)
                        listaEncontrados.append(usuarios1)

        estructuraTablas = ''
        estructura_filas = ''
        estructuraTotal = ''
        for b in listaEncontrados:
            estructuraTablas += f'''
    <p>{b.usuario} </p> 
    <table style="width:100%">
    <tr>
        <th>Mensaje</th>
    '''     
            estructura_filas += f'''
    <tr>
    <td>{b.fechaHora}</td>'''
            
            for c in b.listaProbabilidadesCalulados:
                estructuraTablas += f'''
        <th>%probabilidad perfil “{c.perfil}”</th>
                ''' 
                estructura_filas += f'''<td>{str(c.porcentaje)} %</td>''' 
            estructura_filas += f'</tr>'
            estructuraTablas += f'</tr>' 
            estructuraTotal += estructuraTablas +estructura_filas+f'</table>'

        print(estructuraTotal)
        return jsonify({"lista":estructuraTotal}) 
    except:
        return jsonify({"lista": "Ha ocurrido un error"})

if __name__=='_main_':
    app.run()
#https://github.com/Teitan67/IPC2_EJEMPLO_PY3/blob/main/backend/main.py
#Ejemplo
#http://localhost:5000/UsuarioConectado?nombreUser=Oscar Leon

#flask --app hello run
#Flask --app Backend\app.py run