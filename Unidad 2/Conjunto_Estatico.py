"""Conjunto con capacidad máxima estática."""

from array import array


class ConjuntoEstatico:
    """Conjunto de enteros de capacidad prefijada."""

    def __init__(self, capacidad: int) -> None:
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser positiva.")
        self._capacidad: int = capacidad
        self._elementos: array[int] = array("i")

    def agregar(self, elemento: int) -> bool:
        """Inserta un elemento garantizando unicidad y límite de capacidad."""
        if elemento in self._elementos:
            return False  # Evita duplicados

        if len(self._elementos) >= self._capacidad:
            raise OverflowError("Conjunto lleno: Capacidad alcanzada.")

        self._elementos.append(elemento)
        return True

    def __repr__(self) -> str:
        return f"ConjuntoEstatico(elementos={list(self._elementos)})"


# Ejemplo de uso
if __name__ == "__main__":
    conjunto = ConjuntoEstatico(capacidad=3)

    print(f"Insertar 100: {conjunto.agregar(100)}")  # True
    print(f"Insertar 200: {conjunto.agregar(200)}")  # True
    print(f"Insertar 100 (Duplicado): {conjunto.agregar(100)}")  # False

    print(conjunto)

    try:
        conjunto.agregar(300)
        conjunto.agregar(400)  # Lanza excepción de capacidad
    except OverflowError as error:
        print(f"Excepción capturada: {error}")