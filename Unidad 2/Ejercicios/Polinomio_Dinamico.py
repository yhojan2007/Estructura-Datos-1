class NodoPolinomio:
    """Clase que representa un nodo en un polinomio dinámico."""
    def __init__(self, coeficiente: float, exponente: int) -> None:
        self.coeficiente: float = coeficiente
        self.exponente: int = exponente
        self.siguiente: NodoPolinomio | None = None

class PolinomioDinamico:
    """Clase que representa un polinomio dinámico usando una lista enlazada."""
    def __init__(self) -> None:
        self.cabeza: NodoPolinomio | None = None

    def agregar_termino(self, coeficiente: float, exponente: int) -> None:
        nuevo_termino = NodoPolinomio(coeficiente, exponente)
        if self.cabeza is None or self.cabeza.exponente < exponente:
            nuevo_termino.siguiente = self.cabeza
            self.cabeza = nuevo_termino
        else:
            actual = self.cabeza
            while actual.siguiente is not None and actual.siguiente.exponente > exponente:
                actual = actual.siguiente
            if actual.siguiente is not None and actual.siguiente.exponente == exponente:
                actual.siguiente.coeficiente += coeficiente
            else:
                nuevo_termino.siguiente = actual.siguiente
                actual.siguiente = nuevo_termino

    def evaluar(self, x: float) -> float:
        resultado = 0.0
        actual = self.cabeza
        while actual is not None:
            resultado += actual.coeficiente * (x ** actual.exponente)
            actual = actual.siguiente
        return resultado

    def sumar(self, otro: PolinomioDinamico) -> PolinomioDinamico:
        if otro is None:
            return self
        resultado = PolinomioDinamico()
        actual1 = self.cabeza
        actual2 = otro.cabeza

        while actual1 is not None or actual2 is not None:
            if actual1 is None:
                resultado.agregar_termino(actual2.coeficiente, actual2.exponente)
                actual2 = actual2.siguiente
            elif actual2 is None:
                resultado.agregar_termino(actual1.coeficiente, actual1.exponente)
                actual1 = actual1.siguiente
            elif actual1.exponente > actual2.exponente:
                resultado.agregar_termino(actual1.coeficiente, actual1.exponente)
                actual1 = actual1.siguiente
            elif actual1.exponente < actual2.exponente:
                resultado.agregar_termino(actual2.coeficiente, actual2.exponente)
                actual2 = actual2.siguiente
            else:
                suma_coeficiente = actual1.coeficiente + actual2.coeficiente
                if suma_coeficiente != 0:
                    resultado.agregar_termino(suma_coeficiente, actual1.exponente)
                actual1 = actual1.siguiente
                actual2 = actual2.siguiente

        return resultado

    

    def grado(self) -> int:
        if self.cabeza is None:
            return -1  # Polinomio nulo
        return self.cabeza.exponente


    def derivar(self) -> PolinomioDinamico:
        resultado = PolinomioDinamico()
        actual = self.cabeza
        while actual is not None:
            if actual.exponente > 0:
                resultado.agregar_termino(actual.coeficiente * actual.exponente, actual.exponente - 1)
            actual = actual.siguiente
        return resultado

    def __str__(self) -> str:
        if self.cabeza is None:
            return "0"
        resultado = []
        actual = self.cabeza
        while actual is not None:
            if actual.coeficiente != 0:
                resultado.append(f"{actual.coeficiente}x^{actual.exponente}")
            actual = actual.siguiente
        return " + ".join(resultado) if resultado else "0"


if __name__ == "__main__":
    # Ejemplo de uso
    polinomio1 = PolinomioDinamico()
    polinomio1.agregar_termino(3, 2)  # 3x^2
    polinomio1.agregar_termino(5, 1)  # 5x^1
    polinomio1.agregar_termino(2, 0)  # 2

    polinomio2 = PolinomioDinamico()
    polinomio2.agregar_termino(4, 3)  # 4x^3
    polinomio2.agregar_termino(-3, 2) # -3x^2
    polinomio2.agregar_termino(1, 0)  # 1

    print("Polinomio 1:", polinomio1)
    print("Polinomio 2:", polinomio2)

    suma = polinomio1.sumar(polinomio2)
    print("Suma:", suma)

    derivada = polinomio1.derivar()
    print("Derivada del Polinomio 1:", derivada)

    valor_evaluado = polinomio1.evaluar(2)
    print("Evaluación del Polinomio 1 en x=2:", valor_evaluado)