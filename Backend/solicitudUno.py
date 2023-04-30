class Perfil:
    def __init__(self, nombre, listaPalabrasClave):
        self.nombre = nombre
        self.listaPalabrasClave = listaPalabrasClave

    def getNombre(self):
        return self.nombre
    
    def getListaPalabrasClave(self):
        return self.listaPalabrasClave
    
    def setNombre(self,nombre):
        self.nombre = nombre
    
    def setListaPaClave(self, listaPalabrasClave):
        self.listaPalabrasClave = listaPalabrasClave
#Borrar la clase descartada
class Descartada:
    def __init__(self, listaPalabrasDescartadas):
        self.listaPalabrasDescartadas = listaPalabrasDescartadas

    def getListPalabrasDescartadas(self):
        return self.listaPalabrasDescartadas
    
    def setListPalabrasDescartadas(self, listaPalabrasDescartadas):
        self.listaPalabrasDescartadas = listaPalabrasDescartadas