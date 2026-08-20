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
