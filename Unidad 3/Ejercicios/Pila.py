class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente: Nodo | None = None

class Pila:
    def __init__(self):
        self.tope: Nodo | None = None
        self._tamano = 0
        
    def apilar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.tope is None:
            self.tope = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.tope
            self.tope = nuevo_nodo
            self._tamano = self._tamano + 1
            
    def desapilar(self):
        if self.tope is None:
            return None
        else:
            dato = self.tope
            self.tope = self.tope.siguiente
            self._tamano = self._tamano - 1
            return dato.dato

