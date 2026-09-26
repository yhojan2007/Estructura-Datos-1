class Nodo:
    """Clase que representa un nodo en una lista enlazada simple."""
    def __init__(self, valor: int) -> None:
        self.valor: int = valor
        self.siguiente: Nodo | None = None


class ListaSimple:
    """Clase que representa una lista enlazada simple."""
    def __init__(self) -> None:
        self.cabeza: Nodo | None = None
        self._tamano: int = 0

    def __len__(self):
        """Devuelve el tamaño de la lista enlazada simple."""
        return self._tamano

    def buscar(self, valor: int) -> bool:
        """Busca un valor en la lista enlazada simple."""
        actual = self.cabeza
        while actual:
            if actual.valor == valor:
                return True
            actual = actual.siguiente
        return False

    def agregar_final(self, valor: int) -> None:
        """Agrega un nuevo nodo con el valor dado al final de la lista."""
        if not self.buscar(valor):
            nuevo_nodo = Nodo(valor)
            if not self.cabeza:
                self.cabeza = nuevo_nodo
            else:
                actual = self.cabeza
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nuevo_nodo
            self._tamano += 1
        else:
            print(f"El valor {valor} ya existe en la lista. No se agregará.")
            
    def agregar_inicio(self, valor: int) -> None:
        """Agrega un nuevo nodo con el valor dado al inicio de la lista."""
        if not self.buscar(valor):
            nuevo_nodo = Nodo(valor)
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
            self._tamano += 1
        else:
            print(f"El valor {valor} ya existe en la lista. No se agregará.")

    def eliminar(self, valor: int) -> None:
        """Elimina el nodo con el valor dado de la lista."""
        if self.cabeza is None:
            return

        if self.cabeza.valor == valor:
            self.cabeza = self.cabeza.siguiente
            self._tamano -= 1
            return

        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.valor == valor:
                actual.siguiente = actual.siguiente.siguiente
                self._tamano -= 1
                return
            actual = actual.siguiente
        self._tamano -= 1

    def mostrar(self) -> None:
        """Muestra los valores de la lista enlazada simple."""
        actual = self.cabeza
        while actual:
            print(actual.valor, end=" -> ")
            actual = actual.siguiente
        print("None")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear una lista enlazada simple
    lista = ListaSimple()

    lista.agregar_inicio(30)
    lista.agregar_inicio(20)
    lista.agregar_inicio(10)

    lista.agregar_final(40)
    lista.agregar_final(50)

    lista.mostrar()

    print(f"Tamaño: {len(lista)}")

    print(f"¿Existe 30?: {lista.buscar(30)}")
    print(f"¿Existe 100?: {lista.buscar(100)}")

    # Intentar insertar un repetido
    resultado = lista.agregar_final(30)
    print(f"¿Se insertó 30 nuevamente?: {resultado}")
    lista.mostrar()
    # Eliminar un valor
    print(f"Eliminando el valor 20...")
    lista.eliminar(20)
    print(f"Tamaño: {len(lista)}")
    lista.mostrar()
