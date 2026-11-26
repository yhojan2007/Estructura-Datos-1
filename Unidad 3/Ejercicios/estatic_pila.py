from collections import deque

class Pila:
    """Clase que representa una pila utilizando deque de la biblioteca collections"""
    def __init__(self) -> None:
        self.Pila: deque[int] = deque()

    def apilar(self, dato: int) -> None:
        """agrega un elemento a la pila"""
        self.Pila.append(dato)

    def desapilar(self) -> int | None:
        """elimina y devuelve el elemento en la parte superior de la pila"""
        if not self.Pila:
            return None
        else:
            return self.Pila.pop()