class Mensaje:
    def __init__(self, lugarFecha, usuario, redSocial, textoMensaje):
        self.lugarFecha = lugarFecha
        self.usuario = usuario
        self.redSocial = redSocial
        self.textoMensaje = textoMensaje

    def getLugarFecha(self):
        return self.lugarFecha
    
    def getUsuario(self):
        return self.usuario
    
    def getRedSocial(self):
        return self.redSocial
    
    def getTextoMensaje(self):
        return self.textoMensaje
    
    def setLugarFecha(self,lugarFecha):
        self.lugarFecha = lugarFecha
    
    def setUsuario(self, usuario):
        self.usuario = usuario

    def setRedSocial(self,redSocial):
        self.redSocial = redSocial
    
    def setTextoMensaje(self, textoMensaje):
        self.textoMensaje = textoMensaje