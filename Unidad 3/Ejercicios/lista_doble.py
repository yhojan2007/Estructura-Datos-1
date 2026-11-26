class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente: Nodo | None = None
        self.anterior: Nodo | None = None

class ListaDoble:
    """Clase que representa una lista doblemente enlazada"""
    def __init__(self):
        self.inicio = None
        self.final = None
        self._tamano = 0

    def insert_inicio(self, dato):
        nuevo_nodo=Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.inicio.anterior=nuevo_nodo
            nuevo_nodo.siguiente=self.inicio
            self.inicio = nuevo_nodo

    def insert_final(self, dato):
        nuevo_nodo=Nodo(dato)
        if self.final is None:
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.final
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

    def sacar_inicio(self):
        if self.inicio is None:
            return None
        else: 
            dato = self.inicio.valor
            self.inicio = self.inicio.siguiente
            self.inicio.anterior = None
            return dato
        
    def sacar_final(self):
        if self.final is None:
            return None
        else: 
            dato = self.final.valor
            self.final = self.final.anterior
            self.final.siguiente = None
            return dato
        
    def buscar(self, dato):
        actual = self.inicio
        while actual is not None:
            if actual.valor == dato:
                return True
            actual = actual.siguiente
        return False
