class PolinomioEstatico:
    """Clase que representa un polinomio en un arreglo estático."""
    def __init__(self, grado: int):
        """Inicializa un polinomio de grado dado con coeficientes inicializados a cero."""
        self.grado: int = grado
        self.coeficientes: list[float] = [0] * (grado + 1)

    def agregar_termino(self, coeficiente: float, exponente: int) -> None:
        if exponente < 0 or exponente > self.grado:
            raise ValueError("Exponente fuera de rango.")
        self.coeficientes[exponente] += coeficiente

    def evaluar(self, x: float) -> float:
        resultado = 0.0
        for exponente, coeficiente in enumerate(self.coeficientes):
            resultado += coeficiente * (x ** exponente)
        return resultado

    def sumar(self, otro: PolinomioEstatico) -> PolinomioEstatico:
        if self.grado != otro.grado:
            raise ValueError("Los polinomios deben tener el mismo grado para sumarse.")
        resultado = PolinomioEstatico(self.grado)
        for i in range(self.grado + 1):
            resultado.coeficientes[i] = self.coeficientes[i] + otro.coeficientes[i]
        return resultado

    def grado(self) -> int:
        """Devuelve el grado del polinomio, que es el índice del último coeficiente no nulo."""
        for i in range(self.grado, -1, -1):
            if self.coeficientes[i] != 0:
                return i
        return 0  # Si todos los coeficientes son cero, el grado es 0

    def derivar(self) -> PolinomioEstatico:
        """Devuelve el polinomio derivado."""
        if self.grado == 0:
            return PolinomioEstatico(0)
        resultado = PolinomioEstatico(self.grado - 1)
        for i in range(1, self.grado + 1):
            resultado.coeficientes[i - 1] = i * self.coeficientes[i]
        return resultado

    def mostrar(self) -> str:
        """Devuelve una representación en cadena del polinomio."""
        terminos = []
        for exponente, coeficiente in enumerate(self.coeficientes):
            if coeficiente != 0:
                terminos.append(f"{coeficiente}x^{exponente}")
        return " + ".join(terminos) if terminos else "0"



# Ejemplo de uso
if __name__ == "__main__":
    # Crear un polinomio de grado 3: 5x^3 + 4x^2 + 3x + 2
    polinomio1 = PolinomioEstatico(3)
    polinomio1.agregar_termino(2, 0)  # 2
    polinomio1.agregar_termino(3, 1)  # 3x
    polinomio1.agregar_termino(4, 2)  # 4x^2
    polinomio1.agregar_termino(5, 3)  # 5x^3

    # Crear otro polinomio de grado 3: 2x^3 - 3x + 1
    polinomio2 = PolinomioEstatico(3)
    polinomio2.agregar_termino(1, 0)   # 1
    polinomio2.agregar_termino(-3, 1)  # -3x
    polinomio2.agregar_termino(0, 2)   # 0x^2
    polinomio2.agregar_termino(2, 3)   # 2x^3

    # Sumar los dos polinomios
    suma = polinomio1.sumar(polinomio2)
    # Evaluar la suma en x=2
    suma_evaluada = suma.evaluar(2)
    print("Evaluación de la suma en x=2:", suma_evaluada)
    # Derivar el primer polinomio
    derivada = polinomio1.derivar()
    print("Polinomio 1:", polinomio1.mostrar())
    print("Polinomio 2:", polinomio2.mostrar())
    print("Suma:", suma.mostrar())
    print("Derivada del Polinomio 1:", derivada.mostrar())

