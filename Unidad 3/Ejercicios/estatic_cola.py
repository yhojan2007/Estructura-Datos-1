from collections import deque

class Cola:
    """Clase que representa una cola utilizando deque de la biblioteca collections"""
    def __init__(self) -> None:
        self._cola: deque[int] = deque()

    def encolar(self, dato: int) -> None:
        """agrega un elemento al final de la cola"""
        self._cola.append(dato)

    def desencolar(self) -> int | None:
        """elimina y devuelve el elemento en la parte delantera de la cola"""
        if not self._cola:
            return None
        else:
            return self._cola.popleft()