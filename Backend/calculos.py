import re
from solicitudDos import Probabilidad

def calcularDatos(listPerfiles,palabrasDescartadas,soloMensaje):
    #Primer paso obtener el mensaje
    # Segundo paso eliminar signos 
    mensaje = re.sub(r'[\,\.\\\/\(\)\=\?\¡\¿\'\<\^\>\"\#\%\&\$\#\!\|\¬\°\}\{\]\`\+\*\~\¨\´\[\:\;\-\_]', '', soloMensaje)
    
    #tercer paso separar todas las palabras en una lista sin los espacios
    listapalabras = mensaje.split()
    #print(listapalabras)
    #cuarto paso eliminar las palabras excluidas y tambien eliminar los numeros como digitos
    mensajesinExcluidas = ''
    for cpalabra in listapalabras:
        if cpalabra.lower() in [eliminar.lower() for eliminar in palabrasDescartadas]:
            pass
        else:
            if cpalabra.isdigit():
                pass
            else:  
                mensajesinExcluidas += str(cpalabra)+' ' 
    #print(mensajesinExcluidas)
    
    listapalabrasEncuenta = mensajesinExcluidas.split()
    #print(len(listapalabrasEncuenta))
    totalPalabrasSINEXCLUIDAS = len(listapalabrasEncuenta)
    listaProbabilidades = []

    for i in listPerfiles:
        aux_perfil = i.nombre
        aux_lista = i.listaPalabrasClave
        #print(aux_perfil)
        contadorPalabras = 0
        for j in aux_lista:
            if j.lower() in mensajesinExcluidas.lower():
                #print(j)
                auxiliarListaPalabrasCoincidencia = j.split()
                if len(auxiliarListaPalabrasCoincidencia) > 1: 
                    contadorPalabras += len(auxiliarListaPalabrasCoincidencia)
                else:
                    contadorPalabras += 1
        #print(contadorPalabras)
        resultadoCalculoPorcentajes = calcularPorcentajes(int(totalPalabrasSINEXCLUIDAS),int(contadorPalabras))
        
        resultadoTotal = round(resultadoCalculoPorcentajes, 2)
        #print(resultadoCalculoPorcentajes)

        objetoProbabilidad = Probabilidad(aux_perfil,resultadoTotal)
        listaProbabilidades.append(objetoProbabilidad)
        # Crear una lista donde se almacene la relacion entre el nombre del perfil,porcentaje, mensaje, fecha, lugar, usuario
    return listaProbabilidades

def calcularPorcentajes(totalPalabrasSINEXCLUIDAS,contadorPalabras):
    if totalPalabrasSINEXCLUIDAS !=0:
        resultado = (contadorPalabras/totalPalabrasSINEXCLUIDAS*100)
    else:
        resultado = 0
    return resultado

def calcularPeso(listMensajes, usuarioBuscar):
    suma = 0
    for dato in listMensajes:
        auxListaProbabilidades= dato.listaProbabilidadesCalulados
        buscarCoincidenciaUser =dato.usuario
        if buscarCoincidenciaUser.lower() == usuarioBuscar.lower():
            for dato1 in auxListaProbabilidades:
                auxiliarPerfil = dato1.perfil
                auxiliarPorcentaje = dato1.porcentaje
                #comparar los perfiles, si el perfil actual es igual a los siguientes perfiles entonces hacer calculo de peso
                #luego guardar el peso, junto al perfil, y el usuario en una lista y retornarlo 

    '''
    obtener la lista de probabilidades
    buscar todos los usuarios que correspondan al usuario buscado 
    obtener la lista de probabilidades
    obtener el perfil
    obtener el porcentaje


    lista que tenga usuario, perfil al que corresponde el peso
    '''