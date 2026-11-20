"""
INDEXACIÓN POR CI
==================================================

Objetivo
--------
Demostrar cuánto más rápido es buscar un ciudadano por su CI usando un
ÍNDICE, comparado con revisar los registros uno por uno (escaneo completo).

Estructuras de datos
--------------------
1) ARCHIVO CSV ('ciudadanos.csv'): una fila por ciudadano, los CI no están
   ordenados.

       ci,nombres,apellido_paterno,apellido_materno,fecha_nacimiento,departamento
       10103346,Daniel,Pérez,Pérez,1940-01-09,Pando
       4582193,María,Quispe,Mamani,1990-05-03,La Paz
       7731020,Luis,Rojas,Vaca,2001-08-09,Santa Cruz
       ...

2) `registros` (lista de listas): el CSV ya cargado en memoria. Cada fila es
   una lista de textos y su POSICIÓN en la lista es su "dirección".

       posición   fila
       --------   ------------------------------------------------------------
       0          ['10103346', 'Daniel', 'Pérez', 'Pérez', '1940-01-09', 'Pando']
       1          ['4582193',  'María', 'Quispe', 'Mamani', '1990-05-03', 'La Paz']
       2          ['7731020',  'Luis',  'Rojas',  'Vaca',   '2001-08-09', 'Santa Cruz']
       ...
       N-1        [...]

3) `indice` (diccionario / tabla hash): cada CI apunta a la posición donde está
   su fila en `registros`. No copia los datos, solo guarda la dirección.

       {
           '10103346': 0,
           '4582193':  1,
           '7731020':  2,
           ...
           '9876543':  N-1,
       }

   Buscar un CI en este diccionario es O(1): Python calcula un hash del texto
   y salta directo al lugar donde está guardado, sin importar si hay mil o
   cinco millones de CIs.

Cómo funciona cada búsqueda
---------------------------
SIN índice (escaneo completo, O(n)): se compara el CI de cada fila hasta
encontrarlo. En el peor caso se revisan las N filas.

    fila 0 ¿es 9876543? no
    fila 1 ¿es 9876543? no
    fila 2 ¿es 9876543? no
    ...                                 (hasta N filas)

CON índice (O(1)): se hacen dos saltos directos.

    indice['9876543']  ->  N-1          (1er salto: el diccionario da la posición)
    registros[N-1]     ->  la fila       (2do salto: la lista da la fila)

Nota: el índice tiene un costo único de construcción (un recorrido O(n)) y
ocupa memoria extra; a cambio, cada búsqueda posterior es casi instantánea.
También es un índice de CI ÚNICO: no hay dos ciudadanos con el mismo CI.
"""
import csv
import time

# ---------------------------------------------------------------
# 1) LEER EL CSV  ->  llenar la lista `registros`
# ---------------------------------------------------------------
inicio = time.perf_counter()
with open("ciudadanos.csv", newline="", encoding="utf-8") as f:
    lector = csv.reader(f)
    next(lector)                      # saltar el encabezado (la primera línea)
    registros = list(lector)          # cada fila: [ci, nombres, ap_pat, ap_mat, fecha, depto]
print(f"Leer {len(registros):,} registros: {time.perf_counter() - inicio:.2f} s")

# ---------------------------------------------------------------
# 2) CREAR EL ÍNDICE  ->  diccionario  { CI : posición en `registros` }
#    Ejemplo del resultado: {'10103346': 0, '4582193': 1, '7731020': 2, ...}
# ---------------------------------------------------------------
inicio = time.perf_counter()
indice = {}
for posicion, fila in enumerate(registros):
    ci = fila[0]                      # el CI está en la primera columna
    indice[ci] = posicion             # guardamos: este CI está en esta posición
print(f"Crear índice por CI: {time.perf_counter() - inicio:.2f} s")

# CI a buscar: el último de la lista (el peor caso para la búsqueda sin índice,
# porque hay que revisar todas las filas antes de llegar a él)
ci_buscado = registros[-1][0]
print(f"\nBuscando el CI {ci_buscado}...\n")

# ---------------------------------------------------------------
# 3) BÚSQUEDA SIN ÍNDICE  ->  revisar fila por fila (O(n))
# ---------------------------------------------------------------
inicio = time.perf_counter()
for fila in registros:
    if fila[0] == ci_buscado:         # comparamos el CI de cada fila
        resultado = fila
        break
t_sin = time.perf_counter() - inicio
print(f"Sin índice: {t_sin * 1000:.3f} ms")

# ---------------------------------------------------------------
# 4) BÚSQUEDA CON ÍNDICE  ->  ir directo a la posición (O(1))
#    indice[ci_buscado]  devuelve la posición, por ejemplo 299999
#    registros[299999]   devuelve la fila completa
# ---------------------------------------------------------------
inicio = time.perf_counter()
resultado = registros[indice[ci_buscado]]
t_con = time.perf_counter() - inicio
print(f"Con índice: {t_con * 1000:.6f} ms")

print("Resultado:", resultado)