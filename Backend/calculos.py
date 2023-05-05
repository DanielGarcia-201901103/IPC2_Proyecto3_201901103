import re
from solicitudDos import Probabilidad

def calcularDatos(listPerfiles,palabrasDescartadas,soloMensaje):
    listaPerfilesRealizados = listPerfiles
    excluidas=palabrasDescartadas
    #Primer paso obtener el mensaje
    mensaje = soloMensaje
    # Segundo paso eliminar signos 
    mensaje = re.sub(r'[\,\.\\\/\(\)\=\?\¡\¿\'\<\^\>\"\#\%\&\$\#\!\|\¬\°\}\{\]\`\+\*\~\¨\´\[\:\;\-\_]', '', mensaje)
    
    #tercer paso separar todas las palabras en una lista sin los espacios
    listapalabras = mensaje.split()
    #print(listapalabras)
    #cuarto paso eliminar las palabras excluidas y tambien eliminar los numeros como digitos
    mensajesinExcluidas = ''
    for cpalabra in listapalabras:
        if cpalabra.lower() in [eliminar.lower() for eliminar in excluidas]:
            pass
        else:
            if cpalabra.isdigit():
                pass
            else:  
                mensajesinExcluidas += str(cpalabra)+' ' 
    print(mensajesinExcluidas)
    
    listapalabrasEncuenta = mensajesinExcluidas.split()
    print(len(listapalabrasEncuenta))
    totalPalabrasSINEXCLUIDAS = len(listapalabrasEncuenta)
    listaProbabilidades = []

    for i in listaPerfilesRealizados:
        aux_perfil = i.nombre
        aux_lista =i.listaPalabrasClave
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
        
        resultadoCalculoPorcentajes = round(resultadoCalculoPorcentajes, 2)
        print(resultadoCalculoPorcentajes)

        objetoProbabilidad = Probabilidad(aux_perfil,resultadoCalculoPorcentajes)
        listaProbabilidades.append(objetoProbabilidad)
        # Crear una lista donde se almacene la relacion entre el nombre del perfil,porcentaje, mensaje, fecha, lugar, usuario
    return listaProbabilidades

def calcularPorcentajes(totalPalabrasSINEXCLUIDAS,contadorPalabras):
    if totalPalabrasSINEXCLUIDAS !=0:
        resultado = (contadorPalabras/totalPalabrasSINEXCLUIDAS*100)
    else:
        resultado = 0
    return resultado

def calcularPeso():
    pass