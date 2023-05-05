class Mensaje:
    def __init__(self, lugar, fechaHora, usuario, redSocial, textoMensaje, listaProbabilidadesCalulados):
        self.lugar = lugar
        self.fechaHora = fechaHora
        self.usuario = usuario
        self.redSocial = redSocial
        self.textoMensaje = textoMensaje
        self.listaProbabilidadesCalulados = listaProbabilidadesCalulados

    def getLugar(self):
        return self.lugar
    
    def getFechaHora(self):
        return self.fechaHora
    
    def getUsuario(self):
        return self.usuario
    
    def getRedSocial(self):
        return self.redSocial
    
    def getTextoMensaje(self):
        return self.textoMensaje
    
    def setLugar(self,lugar):
        self.lugar = lugar
    
    def setFechaHora(self, fechaHora):
        self.fechaHora = fechaHora

    def setUsuario(self, usuario):
        self.usuario = usuario

    def setRedSocial(self,redSocial):
        self.redSocial = redSocial
    
    def setTextoMensaje(self, textoMensaje):
        self.textoMensaje = textoMensaje

class Probabilidad:
    def __init__(self, perfil, porcentaje):
        self.perfil = perfil
        self.porcentaje = porcentaje

    def getPerfil(self):
        return self.perfil
    
    def getPorcentaje(self):
        return self.porcentaje
    
    def setPerfil(self, perfil):
        self.perfil = perfil

    def setPorcentaje(self, porcentaje):
        self.porcentaje = porcentaje