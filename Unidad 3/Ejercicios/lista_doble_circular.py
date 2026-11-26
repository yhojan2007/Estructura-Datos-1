class Nodo:
    def __init__(self,valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListDobleCircular:
    def __init__(self):
        self.inicio = None
        self.final = None
        
    def insert_inicio(self, dato):
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
        if self.inicio is None:
            return None
        else: 
            dato = self.inicio.valor
            self.inicio = self.inicio.siguiente
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final
            return dato
        
    def sacar_final(self):
        if self.final is None:
            return None
        else: 
            dato = self.final.valor
            self.final = self.final.anterior
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final
            return dato
    