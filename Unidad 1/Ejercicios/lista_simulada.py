#!/usr/bin/env python3
"""
Representación simulada: lista enlazada sobre un arreglo.

En el modelo simulado no hay punteros reales. Un arreglo estático de
nodos usa índices enteros como si fueran direcciones: ``siguiente``
guarda la posición del sucesor, y ``-1`` representa nulo.

Una lista de libres (cursor) recicla las celdas vacías. Así se imita
el comportamiento dinámico con memoria de tamaño fijo.

Inserción y eliminación en la cabeza: O(1). Búsqueda: O(n).
"""

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")

NULO: int = -1
CAPACIDAD_POR_DEFECTO: int = 8


class ListaSimuladaLlenaError(Exception):
    """Se lanza cuando no quedan celdas libres en el arreglo simulado."""


class ListaSimuladaVaciaError(Exception):
    """Se lanza al eliminar de una lista simulada vacía."""


class NodoSimulado(Generic[T]):
    """
    Celda de la lista simulada.

    ``dato`` es el valor almacenado. ``siguiente`` es un índice del
    arreglo (no una referencia a objeto): funciona como puntero
    simulado. ``NULO`` (-1) equivale a un puntero nulo.
    """

    def __init__(
        self,
        dato: T | None = None,
        siguiente: int = NULO,
    ) -> None:
        self.dato: T | None = dato
        self.siguiente: int = siguiente

    def __str__(self) -> str:
        return f"NodoSimulado(dato={self.dato!r}, siguiente={self.siguiente})"


class ListaSimulada(Generic[T]):
    """
    Lista simplemente enlazada simulada con un arreglo de nodos.

    El arreglo ``_nodos`` es el espacio de memoria. ``_cabeza`` apunta
    (por índice) al primer elemento ocupado. ``_libre`` apunta al
    primer hueco disponible. Al insertar se toma una celda de la lista
    de libres; al eliminar, esa celda se devuelve a los libres.
    """

    def __init__(self, capacidad: int = CAPACIDAD_POR_DEFECTO) -> None:
        if capacidad < 1:
            raise ValueError("La capacidad debe ser un entero positivo.")
        self._capacidad: int = capacidad
        self._nodos: list[NodoSimulado[T]] = [
            NodoSimulado() for _ in range(capacidad)
        ]
        self._cabeza: int = NULO
        self._libre: int = 0
        self._cantidad: int = 0
        self._inicializar_libres()

    def _inicializar_libres(self) -> None:
        """Encadena todas las celdas como lista de espacios disponibles."""
        for indice in range(self._capacidad - 1):
            self._nodos[indice].siguiente = indice + 1
        self._nodos[self._capacidad - 1].siguiente = NULO

    def obtener_capacidad(self) -> int:
        """
        Devuelve cuántas celdas tiene el arreglo simulado.

        Returns:
            int: Tamaño fijo del espacio de nodos.
        """
        return self._capacidad

    def esta_vacia(self) -> bool:
        """
        Indica si no hay elementos ocupados.

        Returns:
            bool: True si la cabeza es el índice nulo.
        """
        return self._cabeza == NULO

    def esta_llena(self) -> bool:
        """
        Indica si la lista de libres se agotó.

        Returns:
            bool: True si no queda ninguna celda reciclable.
        """
        return self._libre == NULO

    def _reservar(self) -> int:
        """
        Toma el primer índice libre y lo saca de la lista de disponibles.

        Returns:
            int: Índice de la celda recién reservada.

        Raises:
            ListaSimuladaLlenaError: Si no hay celdas libres.
        """
        if self.esta_llena():
            raise ListaSimuladaLlenaError(
                "No hay celdas libres en la lista simulada."
            )
        indice = self._libre
        self._libre = self._nodos[indice].siguiente
        return indice

    def _liberar(self, indice: int) -> None:
        """
        Devuelve una celda a la lista de libres y borra su dato.

        Args:
            indice: Posición del arreglo que vuelve a estar disponible.
        """
        self._nodos[indice].dato = None
        self._nodos[indice].siguiente = self._libre
        self._libre = indice

    def insertar_inicio(self, dato: T) -> None:
        """
        Inserta un elemento al inicio usando una celda de la lista libre.

        Args:
            dato: Valor a almacenar en la nueva cabeza.
        """
        indice = self._reservar()
        self._nodos[indice].dato = dato
        self._nodos[indice].siguiente = self._cabeza
        self._cabeza = indice
        self._cantidad += 1

    def insertar_final(self, dato: T) -> None:
        """
        Inserta un elemento al final recorriendo los índices ocupados.

        Args:
            dato: Valor a almacenar en la nueva cola.
        """
        indice = self._reservar()
        self._nodos[indice].dato = dato
        self._nodos[indice].siguiente = NULO
        if self.esta_vacia():
            self._cabeza = indice
        else:
            actual = self._cabeza
            while self._nodos[actual].siguiente != NULO:
                actual = self._nodos[actual].siguiente
            self._nodos[actual].siguiente = indice
        self._cantidad += 1

    def eliminar_inicio(self) -> T:
        """
        Elimina la cabeza y recicla su celda en la lista de libres.

        Returns:
            El valor que estaba al inicio.

        Raises:
            ListaSimuladaVaciaError: Si no hay elementos ocupados.
        """
        if self.esta_vacia():
            raise ListaSimuladaVaciaError(
                "No se puede eliminar: la lista simulada está vacía."
            )
        indice = self._cabeza
        dato = self._nodos[indice].dato
        self._cabeza = self._nodos[indice].siguiente
        self._liberar(indice)
        self._cantidad -= 1
        return dato  # type: ignore[return-value]

    def buscar(self, dato: T) -> bool:
        """
        Recorre los índices ocupados buscando un valor.

        Args:
            dato: Valor a localizar.

        Returns:
            bool: True si alguna celda ocupada contiene el valor.
        """
        actual = self._cabeza
        while actual != NULO:
            if self._nodos[actual].dato == dato:
                return True
            actual = self._nodos[actual].siguiente
        return False

    def mostrar_memoria(self) -> str:
        """
        Describe el arreglo, la cabeza y el primer índice libre.

        Útil para ver cómo los enteros simulan punteros.

        Returns:
            str: Tabla índice / dato / siguiente más los cursores.
        """
        lineas = [
            f"cabeza={self._cabeza}  libre={self._libre}  "
            f"cantidad={self._cantidad}",
            f"{'Índice':<8}{'Dato':<16}{'Siguiente':<10}",
            "-" * 34,
        ]
        for indice, nodo in enumerate(self._nodos):
            lineas.append(
                f"{indice:<8}{str(nodo.dato):<16}{nodo.siguiente:<10}"
            )
        return "\n".join(lineas)

    def __iter__(self) -> Iterator[T]:
        actual = self._cabeza
        while actual != NULO:
            yield self._nodos[actual].dato  # type: ignore[misc]
            actual = self._nodos[actual].siguiente

    def __len__(self) -> int:
        return self._cantidad

    def __str__(self) -> str:
        datos = " -> ".join(repr(dato) for dato in self)
        return f"ListaSimulada[{datos}]"


def demostrar() -> None:
    """Ejecuta una demostración de la lista con representación simulada."""
    lista: ListaSimulada[str] = ListaSimulada(capacidad=5)
    lista.insertar_final("A")
    lista.insertar_final("B")
    lista.insertar_inicio("Z")
    print("Lista lógica:", lista)
    print()
    print("Memoria simulada:")
    print(lista.mostrar_memoria())
    print()
    print("Eliminado al inicio:", lista.eliminar_inicio())
    print("Tras reciclar la celda de 'Z':")
    print(lista.mostrar_memoria())


if __name__ == "__main__":
    demostrar()
