class Nodo:
    """Clase que representa un nodo en una lista doblemente enlazada circular"""
    def __init__(self,valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListDobleCircular:
    """Clase que representa una lista doblemente enlazada circular"""
    def __init__(self):
        self.inicio = None
        self.final = None

    def insert_inicio(self, dato):
        """Inserta un nuevo nodo al inicio de la lista doblemente enlazada circular."""
        nuevo_nodo=Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
            self.inicio.siguiente = self.final
            self.final.siguiente = self.inicio
        else:
            nuevo_nodo.siguiente=self.inicio
            self.inicio.anterior=nuevo_nodo
            self.inicio = nuevo_nodo
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final

    def insert_final(self, dato):
        """Inserta un nuevo nodo al final de la lista doblemente enlazada circular."""
        nuevo_nodo=Nodo(dato)
        if self.final is None:
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
            self.inicio.siguiente = self.final
            self.final.siguiente = self.inicio
        else:
            nuevo_nodo.anterior=self.final
            self.final.siguiente=nuevo_nodo
            self.final = nuevo_nodo
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final

    def sacar_inicio(self):
        """Elimina y devuelve el nodo al inicio de la lista doblemente enlazada circular."""
        if self.inicio is None:
            return None
        else: 
            dato = self.inicio.valor
            self.inicio = self.inicio.siguiente
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final
            return dato
        
    def sacar_final(self):
        """Elimina y devuelve el nodo al final de la lista doblemente enlazada circular."""
        if self.final is None:
            return None
        else: 
            dato = self.final.valor
            self.final = self.final.anterior
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final
            return dato
    