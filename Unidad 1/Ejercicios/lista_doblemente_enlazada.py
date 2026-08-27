#!/usr/bin/env python3
"""
Representación dinámica: lista doblemente enlazada.

En el modelo dinámico cada elemento vive en un nodo independiente,
asignado en tiempo de ejecución. Los nodos se relacionan con
referencias (punteros) ``anterior`` y ``siguiente``, de modo que la
estructura crece y se reduce según se inserten o eliminen datos.

Inserción y eliminación en los extremos: O(1). Búsqueda: O(n).
"""

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class ListaVaciaError(Exception):
    """Se lanza al eliminar o consultar extremos de una lista vacía."""


class NodoDoble(Generic[T]):
    """
    Nodo de una lista doblemente enlazada.

    Guarda un dato y dos enlaces hacia nodos vecinos. Si un enlace vale
    None, ese lado no tiene vecino (inicio o fin de la lista).
    """

    def __init__(self, dato: T) -> None:
        self.dato: T = dato
        self.anterior: NodoDoble[T] | None = None
        self.siguiente: NodoDoble[T] | None = None

    def __str__(self) -> str:
        return f"NodoDoble({self.dato!r})"


class ListaDoblementeEnlazada(Generic[T]):
    """
    Lista lineal dinámica con recorrido en ambos sentidos.

    Mantiene referencias a la cabeza y a la cola para insertar o borrar
    en los extremos sin recorrer toda la cadena. El tamaño no está
    limitado de antemano: cada inserción crea un nodo nuevo.
    """

    def __init__(self) -> None:
        self._cabeza: NodoDoble[T] | None = None
        self._cola: NodoDoble[T] | None = None
        self._cantidad: int = 0

    def esta_vacia(self) -> bool:
        """
        Indica si la lista no tiene nodos.

        Returns:
            bool: True si cabeza y cola no apuntan a ningún nodo.
        """
        return self._cabeza is None

    def insertar_inicio(self, dato: T) -> None:
        """
        Inserta un nodo nuevo al comienzo de la lista.

        Args:
            dato: Valor que almacenará el nodo creado.
        """
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            nuevo.siguiente = self._cabeza
            self._cabeza.anterior = nuevo  # type: ignore[union-attr]
            self._cabeza = nuevo
        self._cantidad += 1

    def insertar_final(self, dato: T) -> None:
        """
        Inserta un nodo nuevo al final de la lista.

        Args:
            dato: Valor que almacenará el nodo creado.
        """
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            nuevo.anterior = self._cola
            self._cola.siguiente = nuevo  # type: ignore[union-attr]
            self._cola = nuevo
        self._cantidad += 1

    def eliminar_inicio(self) -> T:
        """
        Elimina el primer nodo y devuelve su dato.

        Returns:
            El valor que estaba en la cabeza.

        Raises:
            ListaVaciaError: Si la lista no tiene nodos.
        """
        if self.esta_vacia() or self._cabeza is None:
            raise ListaVaciaError("No se puede eliminar: la lista está vacía.")
        dato = self._cabeza.dato
        self._cabeza = self._cabeza.siguiente
        if self._cabeza is None:
            self._cola = None
        else:
            self._cabeza.anterior = None
        self._cantidad -= 1
        return dato

    def eliminar_final(self) -> T:
        """
        Elimina el último nodo y devuelve su dato.

        Returns:
            El valor que estaba en la cola.

        Raises:
            ListaVaciaError: Si la lista no tiene nodos.
        """
        if self.esta_vacia() or self._cola is None:
            raise ListaVaciaError("No se puede eliminar: la lista está vacía.")
        dato = self._cola.dato
        self._cola = self._cola.anterior
        if self._cola is None:
            self._cabeza = None
        else:
            self._cola.siguiente = None
        self._cantidad -= 1
        return dato

    def eliminar(self, dato: T) -> bool:
        """
        Elimina la primera aparición de un valor.

        Args:
            dato: Valor a buscar y quitar de la lista.

        Returns:
            bool: True si se eliminó un nodo; False si no estaba.
        """
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                self._desenlazar(actual)
                return True
            actual = actual.siguiente
        return False

    def _desenlazar(self, nodo: NodoDoble[T]) -> None:
        """
        Quita un nodo ya localizado actualizando los enlaces vecinos.

        Args:
            nodo: Nodo que se retira de la cadena.
        """
        if nodo.anterior is None:
            self._cabeza = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente

        if nodo.siguiente is None:
            self._cola = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior

        self._cantidad -= 1

    def buscar(self, dato: T) -> bool:
        """
        Recorre la lista hacia adelante buscando un valor.

        Args:
            dato: Valor a localizar.

        Returns:
            bool: True si el valor está en algún nodo.
        """
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def hacia_atras(self) -> list[T]:
        """
        Recorre la lista desde la cola hasta la cabeza.

        Returns:
            list: Copia de los datos en orden inverso.
        """
        resultado: list[T] = []
        actual = self._cola
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.anterior
        return resultado

    def __iter__(self) -> Iterator[T]:
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __len__(self) -> int:
        return self._cantidad

    def __str__(self) -> str:
        datos = " <-> ".join(repr(dato) for dato in self)
        return f"ListaDoblementeEnlazada[{datos}]"


def demostrar() -> None:
    """Ejecuta una demostración de la lista doblemente enlazada."""
    lista: ListaDoblementeEnlazada[str] = ListaDoblementeEnlazada()
    lista.insertar_final("B")
    lista.insertar_final("C")
    lista.insertar_inicio("A")
    print("Adelante:", lista)
    print("Atrás:", lista.hacia_atras())
    print("¿Contiene 'B'?", lista.buscar("B"))

    lista.eliminar("B")
    print("Tras eliminar 'B':", lista)
    print("Eliminado al inicio:", lista.eliminar_inicio())
    print("Eliminado al final:", lista.eliminar_final())
    print("¿Vacía?", lista.esta_vacia())


if __name__ == "__main__":
    demostrar()
