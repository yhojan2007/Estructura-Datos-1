# =============================================================================
# Desafío 1 de Copia de Listas
# =============================================================================

# CÓDIGO CORREGIDO
original_data = [10, 20, 30]

# Ahora el estudiante copia los datos de forma independiente
copy_data = original_data.copy() # FIX: Usar .copy() para crear una copia 
                                 # superficial y no una referencia

copy_data.append(40)

print(f"Original: {original_data}")
print(f"Copia: {copy_data}")

# Explicación: Ambos tenían el 40 porque 'copy_data = original_data' 
# asignaba una referencia al mismo objeto en memoria. Cualquier cambio a través de 'copy_data'
# afectaba al objeto original. Al usar 'original_data.copy()', 
# se crea un nuevo objeto de lista en memoria, haciendo que sean independientes.


# ==============================================================================
# Desafío 2 de Implementación de Stack
# ==============================================================================

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        # FIX: Lógica corregida para devolver True si la pila está vacía
        return len(self.items) == 0

    def push(self, item):
        # FIX: Agrega el elemento al final de la lista
        self.items.append(item)

    def pop(self):
        # FIX: Verifica si hay elementos antes de eliminar
        # y retorna el elemento eliminado (LIFO)
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Pop from an empty stack") # Opcional: lanzar un error o devolver None

# --- Prueba del Alumno ---
mi_pila = Stack()
mi_pila.push("A")
mi_pila.push("B")

print("¿Está vacía?", mi_pila.is_empty()) # Esperado: False
print("Elemento sacado:", mi_pila.pop())  # Esperado: B
print("Elemento sacado:", mi_pila.pop())  # Esperado: A
print("¿Está vacía?", mi_pila.is_empty()) # Esperado: True


# =============================================================================
# Desafío 3 de Implementación de Nodo
# =============================================================================

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None # Este es nuestro 'puntero' al siguiente espacio en el Heap

# El estudiante intenta crear una cadena: [Nodo 1] -> [Nodo 2]

# FIX: Crear el primer nodo y asignarlo a 'contenedor' para mantener la referencia al inicio
contenedor = Nodo("Datos Importantes 1")

# FIX: Crear el segundo nodo de forma independiente
segundo_nodo = Nodo("Datos Importantes 2")

# FIX: Enlazar el primer nodo (al que apunta 'contenedor') con el segundo nodo
contenedor.siguiente = segundo_nodo

# Verificación
print(f"Contenido del primer nodo (a través de 'contenedor'): {contenedor.valor}")
if contenedor.siguiente is not None:
    print(f"Contenido del segundo nodo (a través de 'contenedor.siguiente'): {contenedor.siguiente.valor}")
else:
    print("ERROR: El primer nodo no apunta a un segundo nodo.")


# =============================================================================
# Desafío 4 de Implementación de Circunferencia
# =============================================================================

class Punto:
    def __init__(self, x: int | float, y: int | float) -> None:
        self.x: int | float = x
        self.y: int | float = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

class Circunferencia:
    def __init__(self, centro: Punto, radio: int | float) -> None:
        # FIX: Se crea una nueva instancia de Punto para el centro
        # para evitar que modificaciones externas al objeto 'centro' original afecten esta circunferencia.
        self.centro: Punto = Punto(centro.x, centro.y)
        self.radio: int | float = radio

    def __str__(self) -> str:
        return f"Circunferencia con centro en {self.centro} y radio {self.radio}"

# --- Prueba del Alumno ---
mi_punto_original: Punto = Punto(1, 2)
mi_circunferencia: Circunferencia = Circunferencia(mi_punto_original, 5)

print(f"Circunferencia inicial: {mi_circunferencia}")

# El alumno modifica el punto original
mi_punto_original.x = 10
mi_punto_original.y = 20

print(f"Circunferencia después de modificar el punto original: {mi_circunferencia}")


# =============================================================================
# Desafío 5 de Implementación de Garaje
# =============================================================================

class Automovil:
    def __init__(self, marca: str, modelo: str, color: str) -> None:
        self.marca: str = marca
        self.modelo: str = modelo
        self.color: str = color

    def __str__(self) -> str:
        return f"{self.color} {self.marca} {self.modelo}"

class Garaje:
    def __init__(self) -> None:
        self.automoviles: list[Automovil] = []

    def agregar_automovil(self, auto: Automovil) -> None:
        self.automoviles.append(auto)

    def mostrar_automoviles(self) -> None:
        print("Automóviles en el garaje:")
        for i, auto in enumerate(self.automoviles):
            print(f"  {i+1}. {auto}")

# --- Prueba del Alumno ---
mi_garaje: Garaje = Garaje()

# El alumno intenta añadir dos coches diferentes
auto_toyota: Automovil = Automovil("Toyota", "Corolla", "Rojo")
mi_garaje.agregar_automovil(auto_toyota)

# FIX: Crear un NUEVO objeto Automovil para el segundo coche,
# en lugar de modificar y reutilizar la misma variable.
auto_honda: Automovil = Automovil("Honda", "Civic", "Azul")
mi_garaje.agregar_automovil(auto_honda)

mi_garaje.mostrar_automoviles()


# =============================================================================
# Desafío 6 de Implementación de Línea
# =============================================================================

class Punto:
    def __init__(self, x: int | float, y: int | float) -> None:
        self.x: int | float = x
        self.y: int | float = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

class Linea:
    def __init__(self, inicio: Punto, fin: Punto) -> None:
        # FIX: Se crean nuevas instancias de Punto para 'inicio' y 'fin'
        # para asegurar que la Línea sea conceptualmente 'inmutable' y no se afecte por
        # cambios externos a los objetos Punto originales.
        self.inicio: Punto = Punto(inicio.x, inicio.y)
        self.fin: Punto = Punto(fin.x, fin.y)

    def __str__(self) -> str:
        return f"Línea de {self.inicio} a {self.fin}"

# --- Prueba del Alumno ---
punto_a: Punto = Punto(0, 0)
punto_b: Punto = Punto(5, 5)

mi_linea: Linea = Linea(punto_a, punto_b)
print(f"Línea original: {mi_linea}")

# El alumno modifica uno de los puntos originales
punto_a.x = 10
punto_a.y = 10

print(f"Línea después de modificar el punto 'A': {mi_linea}")
