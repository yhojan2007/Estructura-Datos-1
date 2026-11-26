class nodo:
    def __init__(self, dato: int) -> None:
        self.dato: int = dato
        self.siguiente: nodo | None = None
class Cola:
    def __init__(self) -> None:
        self.frente: nodo | None = None
        self.final: nodo | None = None
        self._tamano: int = 0

    def encolar(self, dato: int) -> None:
        """agrega un elemento al final de la cola"""
        nuevo_nodo = nodo(dato)
        if self.frente is None:
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self._tamano = self._tamano + 1

    def desencolar(self) -> int | None:
        if self.frente is None:
            return None
        else:
            dato = self.frente
            self.frente = self.frente.siguiente
            if self.frente is None:
                self.final = None
            self._tamano = self._tamano - 1
            return dato.dato
