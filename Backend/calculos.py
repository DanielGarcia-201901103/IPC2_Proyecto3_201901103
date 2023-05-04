import re
from objetos import Perfil
def calcularPorcentajesYPesos():
    excluidas=['a', 'un', 'una', 'en', 'para', 'por', 'que', 'qué', 'la', 'las', 'los', 'el', 'unas', 'si', 'no', 'sino', 'entre', 
'otro', 'otra', 'otros', 'otras', 'de', 'del', 'nos', 'sus', 'su', 'am', 'pm']
    #Primer paso obtener el mensaje
    mensaje ='''Hola amigos, nos vemos hoy en el gym... recuerden que después vamos a entrenar para 
la carrera 2K del próximo sábado.  No olvieden su Ropa Deportiva y sus bebidas 
Hidratantes.  Recuerden que hoy por la noche juega la selección de fútbol, nos vemos en 
Taco Bell a las 7 pm. ' ?¡?¿!"#$%$&/()='¿|°¬\~``][^{´´-.-,<>'''
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
    perfil1 = 'Deportista'
    listaPerfil1 = ['fútbol', 'balonmano', 'baloncesto', 'balompié', 'football', 'basketball', 'handball', 'estadio', 'selección', 'champions league', 'liga de campeones', 'tenis', 'natación', 'olimpiada', 'gym', 'gimnasio']

    perfil2 = 'Cultura saludable '
    listaPerfil2 = ['gimnasio', 'comida saludable', 'ejercicio', 'maratón', 'carrera', 'entreno', 'entrenar', 'entrenamiento', 'pesas', 'karate', 'tae kwon do', 'boxeo', 'gym', 'healthy food', 'vitaminas', 'caminata', 'caminar', 'ropa deportiva', 'bebida hidratante', 'bebidas hidratantes']
    objeto = Perfil(perfil1,listaPerfil1)
    objeto2 = Perfil(perfil2,listaPerfil2)

    listaPerfilesRealizados = []
    listaPerfilesRealizados.append(objeto)
    listaPerfilesRealizados.append(objeto2)

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
        print(resultadoCalculoPorcentajes)
        # Crear una lista donde se almacene la relacion entre el nombre del perfil,porcentaje, mensaje, fecha, lugar, usuario


def calcularPorcentajes(totalPalabrasSINEXCLUIDAS,contadorPalabras):
    if totalPalabrasSINEXCLUIDAS !=0:
        resultado = (contadorPalabras/totalPalabrasSINEXCLUIDAS*100)

    return resultado

calcularPorcentajesYPesos()
    