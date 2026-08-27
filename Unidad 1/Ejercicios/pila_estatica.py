#!/usr/bin/env python3
"""
Representación estática: pila (stack) de capacidad fija.

En el modelo estático el tamaño se reserva de antemano en un bloque
contiguo de memoria. El arreglo no crece ni se encoge en tiempo de
ejecución: solo se mueve un índice (el tope) sobre ese espacio.

Complejidad de apilar, desapilar y consultar la cima: O(1).
"""

from typing import Generic, TypeVar

T = TypeVar("T")

CAPACIDAD_POR_DEFECTO: int = 8


class PilaLlenaError(Exception):
    """Se lanza al apilar cuando la pila ya alcanzó su capacidad máxima."""


class PilaVaciaError(Exception):
    """Se lanza al desapilar o consultar la cima de una pila vacía."""


class PilaEstatica(Generic[T]):
    """
    Pila LIFO implementada con un arreglo de tamaño fijo.

    El almacenamiento se preasigna en ``__init__``. Las operaciones no
    piden memoria extra: solo actualizan ``_tope``, el índice del último
    elemento válido. Si se intenta apilar con la pila llena se produce
    desbordamiento (overflow).
    """

    def __init__(self, capacidad: int = CAPACIDAD_POR_DEFECTO) -> None:
        if capacidad < 1:
            raise ValueError("La capacidad debe ser un entero positivo.")
        self._capacidad: int = capacidad
        self._elementos: list[T | None] = [None] * capacidad
        self._tope: int = -1

    def obtener_capacidad(self) -> int:
        """
        Devuelve la cantidad máxima de elementos que admite la pila.

        Returns:
            int: Capacidad fija reservada al crear la pila.
        """
        return self._capacidad

    def esta_vacia(self) -> bool:
        """
        Indica si la pila no contiene elementos.

        Returns:
            bool: True si el tope aún no apunta a ninguna posición.
        """
        return self._tope == -1

    def esta_llena(self) -> bool:
        """
        Indica si ya no hay espacio libre en el arreglo estático.

        Returns:
            bool: True si el tope alcanzó la última posición válida.
        """
        return self._tope == self._capacidad - 1

    def apilar(self, elemento: T) -> None:
        """
        Inserta un elemento en la cima (operación push).

        Args:
            elemento: Valor que se coloca en el tope de la pila.

        Raises:
            PilaLlenaError: Si no queda espacio en el arreglo.
        """
        if self.esta_llena():
            raise PilaLlenaError(
                f"No se puede apilar: capacidad máxima de "
                f"{self._capacidad} elementos."
            )
        self._tope += 1
        self._elementos[self._tope] = elemento

    def desapilar(self) -> T:
        """
        Extrae y devuelve el elemento de la cima (operación pop).

        Returns:
            El valor que estaba en el tope.

        Raises:
            PilaVaciaError: Si la pila no tiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("No se puede desapilar: la pila está vacía.")
        elemento = self._elementos[self._tope]
        self._elementos[self._tope] = None
        self._tope -= 1
        return elemento  # type: ignore[return-value]

    def cima(self) -> T:
        """
        Devuelve el elemento de la cima sin extraerlo (operación peek).

        Returns:
            El valor que está en el tope.

        Raises:
            PilaVaciaError: Si la pila no tiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("No se puede consultar la cima: pila vacía.")
        return self._elementos[self._tope]  # type: ignore[return-value]

    def __len__(self) -> int:
        return self._tope + 1

    def __str__(self) -> str:
        if self.esta_vacia():
            return "PilaEstatica([])"
        valores = self._elementos[: self._tope + 1]
        return f"PilaEstatica({valores}, cima={valores[-1]})"


def demostrar() -> None:
    """Ejecuta una demostración de la pila con representación estática."""
    pila: PilaEstatica[str] = PilaEstatica(capacidad=3)
    print("Capacidad fija:", pila.obtener_capacidad())

    pila.apilar("A")
    pila.apilar("B")
    pila.apilar("C")
    print("Pila llena:", pila)
    print("¿Está llena?", pila.esta_llena())

    try:
        pila.apilar("D")
    except PilaLlenaError as error:
        print("Overflow controlado:", error)

    print("Cima:", pila.cima())
    print("Desapilado:", pila.desapilar())
    print("Después de desapilar:", pila)
    print("Cantidad actual:", len(pila))


if __name__ == "__main__":
    demostrar()
