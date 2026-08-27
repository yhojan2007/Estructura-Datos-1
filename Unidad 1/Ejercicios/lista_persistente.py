#!/usr/bin/env python3
"""
Representación persistente: lista guardada en memoria secundaria.

En el modelo persistente los datos no viven solo en RAM. Cada
operación se refleja en un archivo, de modo que la información
sobrevive al cierre del programa.

Esta implementación usa JSON como soporte: es legible y no depende
de punteros en memoria. Los elementos deben ser serializables
(str, int, float, bool, list o dict).

Inserción al final y consulta por índice: O(n) por la lectura del
archivo. Persistencia real: el archivo permanece en disco.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

ARCHIVO_POR_DEFECTO: str = "lista_persistente.json"


class ListaPersistenteVaciaError(Exception):
    """Se lanza al eliminar o consultar una lista persistente vacía."""


class ListaPersistente:
    """
    Lista lineal cuyo estado se almacena en un archivo JSON.

    A diferencia de las representaciones en memoria volátil, aquí el
    medio de almacenamiento es secundario. Al crear la estructura se
    carga el archivo si existe; si no, se crea uno vacío. Cada alta o
    baja reescribe el archivo para mantener la persistencia.
    """

    def __init__(self, ruta: str | Path = ARCHIVO_POR_DEFECTO) -> None:
        self._ruta: Path = Path(ruta)
        self._asegurar_archivo()

    def _asegurar_archivo(self) -> None:
        """Crea el archivo JSON vacío cuando todavía no existe en disco."""
        if not self._ruta.exists():
            self._escribir([])

    def _leer(self) -> list[Any]:
        """
        Carga desde disco la lista completa de elementos.

        Returns:
            list: Elementos persistidos. Si el archivo está dañado,
            se trata como lista vacía y se reescribe.
        """
        try:
            with self._ruta.open(encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (json.JSONDecodeError, OSError):
            datos = []
            self._escribir(datos)
        if not isinstance(datos, list):
            raise TypeError(
                f"El archivo {self._ruta} no contiene una lista JSON."
            )
        return datos

    def _escribir(self, elementos: list[Any]) -> None:
        """
        Reemplaza el contenido del archivo con la lista recibida.

        Args:
            elementos: Secuencia que se serializa a JSON.
        """
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        with self._ruta.open("w", encoding="utf-8") as archivo:
            json.dump(elementos, archivo, ensure_ascii=False, indent=2)

    def obtener_ruta(self) -> Path:
        """
        Devuelve la ruta del archivo que sostiene la persistencia.

        Returns:
            Path: Ubicación del JSON en disco.
        """
        return self._ruta

    def esta_vacia(self) -> bool:
        """
        Indica si el archivo no guarda elementos.

        Returns:
            bool: True si la lista persistida está vacía.
        """
        return len(self._leer()) == 0

    def insertar_final(self, elemento: Any) -> None:
        """
        Agrega un elemento al final y lo persiste en disco.

        Args:
            elemento: Valor JSON-serializable que se anexará.
        """
        elementos = self._leer()
        elementos.append(elemento)
        self._escribir(elementos)

    def insertar_inicio(self, elemento: Any) -> None:
        """
        Agrega un elemento al inicio y lo persiste en disco.

        Args:
            elemento: Valor JSON-serializable que se insertará.
        """
        elementos = self._leer()
        elementos.insert(0, elemento)
        self._escribir(elementos)

    def eliminar_final(self) -> Any:
        """
        Quita el último elemento, actualiza el archivo y lo devuelve.

        Returns:
            El valor eliminado del final.

        Raises:
            ListaPersistenteVaciaError: Si no hay elementos en disco.
        """
        elementos = self._leer()
        if not elementos:
            raise ListaPersistenteVaciaError(
                "No se puede eliminar: la lista persistente está vacía."
            )
        valor = elementos.pop()
        self._escribir(elementos)
        return valor

    def eliminar_inicio(self) -> Any:
        """
        Quita el primer elemento, actualiza el archivo y lo devuelve.

        Returns:
            El valor eliminado del inicio.

        Raises:
            ListaPersistenteVaciaError: Si no hay elementos en disco.
        """
        elementos = self._leer()
        if not elementos:
            raise ListaPersistenteVaciaError(
                "No se puede eliminar: la lista persistente está vacía."
            )
        valor = elementos.pop(0)
        self._escribir(elementos)
        return valor

    def buscar(self, elemento: Any) -> bool:
        """
        Busca un valor entre los datos persistidos.

        Args:
            elemento: Valor a localizar.

        Returns:
            bool: True si el valor está guardado en el archivo.
        """
        return elemento in self._leer()

    def obtener(self, indice: int) -> Any:
        """
        Devuelve el elemento almacenado en una posición.

        Args:
            indice: Posición basada en cero.

        Returns:
            El valor persistido en esa posición.

        Raises:
            IndexError: Si el índice queda fuera de rango.
        """
        elementos = self._leer()
        if indice < 0 or indice >= len(elementos):
            raise IndexError(
                f"Índice {indice} fuera de rango (tamaño={len(elementos)})."
            )
        return elementos[indice]

    def vaciar(self) -> None:
        """Borra todos los elementos y deja el archivo como lista vacía."""
        self._escribir([])

    def __iter__(self) -> Iterator[Any]:
        yield from self._leer()

    def __len__(self) -> int:
        return len(self._leer())

    def __str__(self) -> str:
        return f"ListaPersistente({self._leer()!r}, archivo={self._ruta})"


def demostrar() -> None:
    """Ejecuta una demostración de la lista con representación persistente."""
    ruta = Path(__file__).with_name("_demo_lista_persistente.json")
    lista = ListaPersistente(ruta)
    lista.vaciar()

    lista.insertar_final("uno")
    lista.insertar_final("dos")
    lista.insertar_inicio("cero")
    print("Lista en disco:", lista)
    print("Ruta:", lista.obtener_ruta())
    print("¿Contiene 'dos'?", lista.buscar("dos"))
    print("Elemento en índice 1:", lista.obtener(1))
    print("Eliminado al final:", lista.eliminar_final())
    print("Estado persistido:", lista)
    print("El archivo sigue existiendo al terminar el programa.")


if __name__ == "__main__":
    demostrar()
