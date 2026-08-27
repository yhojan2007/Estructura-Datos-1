"""Conjunto dinámico basado en Tabla Hash."""

from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class ConjuntoDinamico(Generic[T]):
    """Conjunto dinámico con redimensionamiento automático."""

    _DUMMY = object()  # Tombstone para celdas eliminadas

    def __init__(self, capacidad_inicial: int = 4) -> None:
        self._capacidad: int = capacidad_inicial
        self._tabla: list[Optional[object]] = [None] * self._capacidad
        self._tamanio: int = 0

    def _hash(self, clave: T) -> int:
        return hash(clave) % self._capacidad

    def _redimensionar(self) -> None:
        """Duplica el tamaño de la tabla cuando el factor de carga es alto."""
        elementos = [x for x in self._tabla if x is not None and x is not self._DUMMY]
        self._capacidad *= 2
        self._tabla = [None] * self._capacidad
        self._tamanio = 0

        for elem in elementos:
            self.agregar(elem)  # type: ignore[arg-type]

    def agregar(self, elemento: T) -> bool:
        """Agrega un elemento garantizando unicidad en O(1) promedio."""
        if (self._tamanio + 1) / self._capacidad > 0.6:
            self._redimensionar()

        idx = self._hash(elemento)
        primer_dummy: Optional[int] = None

        while self._tabla[idx] is not None:
            if self._tabla[idx] == elemento:
                return False
            if self._tabla[idx] is self._DUMMY and primer_dummy is None:
                primer_dummy = idx
            idx = (idx + 1) % self._capacidad

        pos = primer_dummy if primer_dummy is not None else idx
        self._tabla[pos] = elemento
        self._tamanio += 1
        return True

    def obtener_elementos(self) -> list[T]:
        """Regresa una lista limpia con los elementos del conjunto."""
        return [x for x in self._tabla if x is not None and x is not self._DUMMY]  # type: ignore[misc]

    def __repr__(self) -> str:
        return f"ConjuntoDinamico(elementos={self.obtener_elementos()})"


# Ejemplo de uso
if __name__ == "__main__":
    conjunto_din: ConjuntoDinamico[str] = ConjuntoDinamico(capacidad_inicial=2)

    # Inserción con expansión automática de la tabla interna
    conjunto_din.agregar("Python")
    conjunto_din.agregar("Go")
    conjunto_din.agregar("Rust")  # Activa redimensionamiento

    print(conjunto_din)  # ConjuntoDinamico(elementos=['Python', 'Go', 'Rust'])
    print(f"¿Agregar duplicado 'Python'?: {conjunto_din.agregar('Python')}")  # False