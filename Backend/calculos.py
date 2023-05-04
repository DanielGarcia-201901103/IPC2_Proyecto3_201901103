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
    print(listapalabras)
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
    