# INF-220 | Estructura de Datos I

Ejercicios, prácticas y proyectos de **estructuras de datos** implementados en **Python**.

## Requisitos

- Python 3.10 o superior

## Cómo ejecutar

Desde la raíz del repositorio:

```bash
python "Unidad 2/Ejercicios/Polinomio_Estatico.py"
```

Reemplaza la ruta por el ejercicio que quieras probar. La mayoría de los scripts incluye un bloque `if __name__ == "__main__"` con una demostración.

## Estructura del proyecto

```
Estructura de datos 1/
├── Unidad 0/          ← Estándares y buenas prácticas
├── Unidad 1/          ← Modelos de representación de datos
├── Unidad 2/          ← ADT polinomio, conjuntos y matriz dispersa
├── Unidad 3/          ← Listas, pilas y colas
├── Indexacion/        ← Índice por CI sobre CSV
├── Proyectos/         ← Enlaces a proyectos aplicados
└── README.md
```

## Contenido por unidad

### [Unidad 0](Unidad%200/README.md) · Estándares y buenas prácticas

| Archivo | Descripción |
|---------|-------------|
| `Ejercicios/Verificador_Calidad.py` | Analiza código Python (docstrings, PEP 8, type hints) |
| `Ejercicios/InterfazABC.py` | Interfaz abstracta `EstructuraLineal` con pila y cola |

### [Unidad 1](Unidad%201/README.md) · Modelos de representación de datos

| Archivo | Descripción |
|---------|-------------|
| `Ejercicios/pila_estatica.py` | Pila con almacenamiento de capacidad fija |
| `Ejercicios/lista_simulada.py` | Lista simulada sobre arreglo |
| `Ejercicios/lista_doblemente_enlazada.py` | Lista doblemente enlazada |
| `Ejercicios/lista_persistente.py` | Lista persistente en disco |
| `Ejercicios/Desafios.py` | Desafíos de copia, stack, nodos y referencias |

### [Unidad 2](Unidad%202/README.md) · ADT polinomio, conjuntos y matriz dispersa

| Archivo | Descripción |
|---------|-------------|
| `Ejercicios/Polinomio_Estatico.py` | Polinomio con arreglo de coeficientes |
| `Ejercicios/Polinomio_Dinamico.py` | Polinomio con lista enlazada de términos |
| `Ejercicios/Conjunto_Estatico.py` | Conjunto de enteros con capacidad fija |
| `Ejercicios/Conjunto_Dinamico.py` | Conjunto genérico con tabla hash |

Detalle de operaciones y pendientes (matriz dispersa): ver [Unidad 2/README.md](Unidad%202/README.md).

### [Unidad 3](Unidad%203/README.md) · Listas, pilas y colas

| Archivo | Descripción |
|---------|-------------|
| `Ejercicios/Lista_simple.py` | Lista simplemente enlazada |
| `Ejercicios/lista_doble.py` | Lista doblemente enlazada |
| `Ejercicios/lista_doble_circular.py` | Lista doblemente circular |
| `Ejercicios/Pila.py` | Pila dinámica (nodos) |
| `Ejercicios/Cola.py` | Cola dinámica (nodos) |
| `Ejercicios/estatic_pila.py` | Pila estática |
| `Ejercicios/estatic_cola.py` | Cola estática |

### Indexación

| Archivo | Descripción |
|---------|-------------|
| `Indexacion/indexacion.py` | Búsqueda por CI: escaneo lineal vs índice (tabla hash) |
| `Indexacion/scrip_ciudanos_csv.py` | Utilidad relacionada con `ciudadanos.csv` |
| `ciudadanos.csv` | Dataset de ciudadanos usado en la práctica |

### [Proyectos](Proyectos/README.md)

Aplicaciones que usan las estructuras del curso:

| Proyecto | Stack | Repo |
|----------|-------|------|
| Polinomio MVC | Python, Flask | [Polinomio-MVC](https://github.com/yhojan2007/Polinomio-MVC-Flask.) |
| Notepad App | Python, Kivy | [Notepad](https://github.com/yhojan2007/kivy-notepad-app) |

## Autor

- GitHub: [@yhojan2007](https://github.com/yhojan2007)
- LinkedIn: [Yhojan Mendoza](https://www.linkedin.com/in/yhojan-mendoza-113b5a423/)
