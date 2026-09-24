#!/usr/bin/env python3
"""
Conjunto estático de enteros con capacidad máxima prefijada.

El almacenamiento es un arreglo de tamaño acotado: no hay
redimensionamiento. Las operaciones de conjunto (unión, intersección
y diferencia) devuelven un conjunto nuevo y no mutan los operandos.
"""

from __future__ import annotations

from array import array


class ConjuntoEstatico:
    """
    Conjunto de enteros con unicidad y capacidad fija.

    Internamente usa ``array('i')``. Insertar un duplicado no altera
    el conjunto. Insertar con la capacidad agotada produce overflow.
    """

    def __init__(self, capacidad: int) -> None:
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser positiva.")
        self._capacidad: int = capacidad
        self._elementos: array[int] = array("i")

    def agregar(self, elemento: int) -> bool:
        """
        Inserta un entero si no está y queda espacio.

        Args:
            elemento: Valor a incorporar al conjunto.

        Returns:
            bool: True si se insertó; False si ya pertenecía.

        Raises:
            OverflowError: Si el conjunto ya alcanzó su capacidad.
        """
        if self.contiene(elemento):
            return False
        if len(self._elementos) >= self._capacidad:
            raise OverflowError("Conjunto lleno: capacidad alcanzada.")
        self._elementos.append(elemento)
        return True

    def quitar(self, elemento: int) -> bool:
        """
        Elimina un entero si pertenece al conjunto.

        Args:
            elemento: Valor a retirar.

        Returns:
            bool: True si se eliminó; False si no estaba.
        """
        if not self.contiene(elemento):
            return False
        self._elementos.remove(elemento)
        return True

    def contiene(self, elemento: int) -> bool:
        """
        Indica si un entero pertenece al conjunto.

        Args:
            elemento: Valor a consultar.

        Returns:
            bool: True si el elemento está almacenado.
        """
        return elemento in self._elementos

    def union(self, otro: ConjuntoEstatico) -> ConjuntoEstatico:
        """
        Calcula la unión de este conjunto con otro (A ∪ B).

        El resultado tiene capacidad igual a la suma de ambas
        capacidades, suficiente para el peor caso sin elementos
        repetidos.

        Args:
            otro: Segundo operando de la unión.

        Returns:
            ConjuntoEstatico: Nuevo conjunto con los elementos de A y B.
        """
        self._asegurar_conjunto(otro)
        resultado = ConjuntoEstatico(self._capacidad + otro._capacidad)
        for elemento in self._elementos:
            resultado.agregar(elemento)
        for elemento in otro._elementos:
            resultado.agregar(elemento)
        return resultado

    def interseccion(self, otro: ConjuntoEstatico) -> ConjuntoEstatico:
        """
        Calcula la intersección de este conjunto con otro (A ∩ B).

        Args:
            otro: Segundo operando de la intersección.

        Returns:
            ConjuntoEstatico: Nuevo conjunto con los elementos comunes.
        """
        self._asegurar_conjunto(otro)
        resultado = ConjuntoEstatico(max(1, min(self._capacidad, otro._capacidad)))
        for elemento in self._elementos:
            if otro.contiene(elemento):
                resultado.agregar(elemento)
        return resultado

    def diferencia(self, otro: ConjuntoEstatico) -> ConjuntoEstatico:
        """
        Calcula la diferencia de este conjunto con otro (A − B).

        Args:
            otro: Conjunto cuyos elementos se excluyen.

        Returns:
            ConjuntoEstatico: Nuevo conjunto con los de A que no están en B.
        """
        self._asegurar_conjunto(otro)
        resultado = ConjuntoEstatico(self._capacidad)
        for elemento in self._elementos:
            if not otro.contiene(elemento):
                resultado.agregar(elemento)
        return resultado

    def es_subconjunto(self, otro: ConjuntoEstatico) -> bool:
        """
        Indica si este conjunto es subconjunto del otro (A ⊆ B).

        El conjunto vacío se considera subconjunto de cualquier conjunto.

        Args:
            otro: Conjunto contra el que se compara.

        Returns:
            bool: True si todo elemento de A también está en B.
        """
        self._asegurar_conjunto(otro)
        for elemento in self._elementos:
            if not otro.contiene(elemento):
                return False
        return True

    def _asegurar_conjunto(self, otro: ConjuntoEstatico) -> None:
        """
        Verifica en tiempo de ejecución que el operando sea un conjunto.

        Args:
            otro: Valor recibido en una operación binaria.

        Raises:
            TypeError: Si ``otro`` no es un ConjuntoEstatico.
        """
        if not isinstance(otro, ConjuntoEstatico):
            raise TypeError("El operando debe ser un ConjuntoEstatico.")

    def __len__(self) -> int:
        return len(self._elementos)

    def __contains__(self, elemento: object) -> bool:
        return isinstance(elemento, int) and self.contiene(elemento)

    def __repr__(self) -> str:
        return f"ConjuntoEstatico(elementos={list(self._elementos)})"


# Demostración de las operaciones del conjunto estático
def demostrar() -> None:
    """Ejecuta una demostración de las operaciones del conjunto estático."""
    conjunto_a = ConjuntoEstatico(capacidad=5)
    conjunto_b = ConjuntoEstatico(capacidad=5)

    conjunto_a.agregar(1)
    conjunto_a.agregar(2)
    conjunto_a.agregar(3)

    conjunto_b.agregar(3)
    conjunto_b.agregar(4)
    conjunto_b.agregar(5)

    print("A:", conjunto_a)
    print("B:", conjunto_b)
    print("¿A contiene 2?", conjunto_a.contiene(2))
    print("Unión A ∪ B:", conjunto_a.union(conjunto_b))
    print("Intersección A ∩ B:", conjunto_a.interseccion(conjunto_b))
    print("Diferencia A − B:", conjunto_a.diferencia(conjunto_b))
    print("¿A ⊆ B?", conjunto_a.es_subconjunto(conjunto_b))

    print("Quitar 2 de A:", conjunto_a.quitar(2))
    print("Quitar 9 de A (ausente):", conjunto_a.quitar(9))
    print("A después de quitar:", conjunto_a)


if __name__ == "__main__":
    demostrar()
