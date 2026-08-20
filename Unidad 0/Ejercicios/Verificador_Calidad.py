#!/usr/bin/env python3
"""
Módulo de verificación automática de calidad de código.

Este script analiza archivos Python en busca de:
- Docstrings faltantes en clases, funciones y métodos
- Nombres no válidos (contra convenciones PEP 8)
- Funciones públicas sin type hints

Puede ejecutarse sobre archivos individuales o directorios completos.
"""

import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import argparse


# ============================================================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================================================

class Severidad(Enum):
    """Niveles de severidad para los problemas encontrados."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Problema:
    """
    Representa un problema encontrado en el código.
    
    Attributes:
        archivo (str): Ruta del archivo.
        linea (int): Número de línea.
        columna (int): Número de columna.
        severidad (Severidad): Nivel de severidad.
        categoria (str): Categoría del problema.
        mensaje (str): Descripción del problema.
        sugerencia (Optional[str]): Sugerencia de corrección.
    """
    archivo: str
    linea: int
    columna: int
    severidad: Severidad
    categoria: str
    mensaje: str
    sugerencia: Optional[str] = None
    
    def __str__(self) -> str:
        """Formatea el problema para salida en consola."""
        emoji = {
            Severidad.ERROR: "❌",
            Severidad.WARNING: "⚠️",
            Severidad.INFO: "ℹ️"
        }.get(self.severidad, "•")
        
        return (
            f"{emoji} {self.archivo}:{self.linea}:{self.columna} "
            f"[{self.severidad.value}] {self.categoria}\n"
            f"   {self.mensaje}"
            f"{f'\n   💡 {self.sugerencia}' if self.sugerencia else ''}"
        )


@dataclass
class Estadisticas:
    """
    Estadísticas del análisis.
    
    Attributes:
        total_archivos (int): Número de archivos analizados.
        total_problemas (int): Número total de problemas.
        problemas_por_severidad (Dict[Severidad, int]): Conteo por severidad.
        problemas_por_categoria (Dict[str, int]): Conteo por categoría.
        archivos_limpios (int): Número de archivos sin problemas.
    """
    total_archivos: int = 0
    total_problemas: int = 0
    problemas_por_severidad: Dict[Severidad, int] = field(default_factory=dict)
    problemas_por_categoria: Dict[str, int] = field(default_factory=dict)
    archivos_limpios: int = 0
    
    def __post_init__(self) -> None:
        """Inicializa los contadores."""
        for severidad in Severidad:
            self.problemas_por_severidad[severidad] = 0


# ============================================================================
# ANALIZADOR DE CÓDIGO
# ============================================================================

class AnalizadorCodigo(ast.NodeVisitor):
    """
    Analizador AST para verificar calidad del código.
    
    Este visitante recorre el árbol sintáctico y verifica:
    - Docstrings en clases, funciones y métodos
    - Convenciones de nombres (PEP 8)
    - Type hints en funciones públicas
    
    Attributes:
        archivo (str): Ruta del archivo actual.
        contenido (str): Contenido del archivo.
        problemas (List[Problema]): Lista de problemas encontrados.
        nombres_privados (Set[str]): Conjunto de nombres privados.
    """
    
    # Patrones para validación de nombres (PEP 8)
    PATRON_CLASE = re.compile(r'^[A-Z][a-zA-Z0-9]+$')
    PATRON_FUNCION = re.compile(r'^[a-z][a-z0-9_]*$')
    PATRON_CONSTANTE = re.compile(r'^[A-Z][A-Z0-9_]*$')
    PATRON_PRIVADO = re.compile(r'^_[a-z][a-z0-9_]*$')
    PATRON_ESPECIAL = re.compile(r'^__[a-z][a-z0-9_]*__$')
    
    # Nombres de métodos especiales permitidos
    METODOS_ESPECIALES = {
        '__init__', '__str__', '__repr__', '__len__', '__iter__',
        '__contains__', '__getitem__', '__setitem__', '__delitem__',
        '__enter__', '__exit__', '__call__', '__add__', '__sub__',
        '__mul__', '__truediv__', '__eq__', '__ne__', '__lt__',
        '__le__', '__gt__', '__ge__', '__hash__', '__bool__'
    }
    
    def __init__(self, archivo: str, contenido: str) -> None:
        """
        Inicializa el analizador.
        
        Args:
            archivo (str): Ruta del archivo.
            contenido (str): Contenido del archivo.
        """
        super().__init__()
        self.archivo = archivo
        self.contenido = contenido
        self.problemas: List[Problema] = []
        self.nombres_privados: Set[str] = set()
        self._en_metodo_especial: bool = False
    
    def verificar(self, arbol: ast.AST) -> List[Problema]:
        """
        Ejecuta la verificación sobre el AST.
        
        Args:
            arbol (ast.AST): Árbol sintáctico.
        
        Returns:
            List[Problema]: Lista de problemas encontrados.
        """
        self.visit(arbol)
        return self.problemas
    
    # ========================================================================
    # VISITORES DE NODOS
    # ========================================================================
    
    def visit_ClassDef(self, nodo: ast.ClassDef) -> None:
        """
        Verifica clases.
        
        - Docstring
        - Nombre (CamelCase)
        """
        # Verificar docstring
        self._verificar_docstring(
            nodo,
            categoria="Docstring de clase",
            mensaje_faltante=f"La clase '{nodo.name}' no tiene docstring"
        )
        
        # Verificar nombre
        if not self._es_nombre_valido_clase(nodo.name):
            self._agregar_problema(
                nodo.lineno,
                nodo.col_offset,
                Severidad.WARNING,
                "Nombre de clase inválido",
                f"La clase '{nodo.name}' no sigue CamelCase",
                f"Renombrar a '{self._sugerir_nombre_clase(nodo.name)}'"
            )
        
        # Verificar métodos
        self.generic_visit(nodo)
    
    def visit_FunctionDef(self, nodo: ast.FunctionDef) -> None:
        """
        Verifica funciones y métodos.
        
        - Docstring
        - Nombre (snake_case)
        - Type hints (funciones públicas)
        """
        # Verificar si es método especial
        es_metodo_especial = nodo.name in self.METODOS_ESPECIALES
        
        # Verificar docstring
        if not es_metodo_especial:
            self._verificar_docstring(
                nodo,
                categoria="Docstring de función",
                mensaje_faltante=f"La función '{nodo.name}' no tiene docstring"
            )
        
        # Verificar nombre
        if not es_metodo_especial and not self._es_nombre_valido_funcion(nodo.name):
            self._agregar_problema(
                nodo.lineno,
                nodo.col_offset,
                Severidad.WARNING,
                "Nombre de función inválido",
                f"La función '{nodo.name}' no sigue snake_case",
                f"Renombrar a '{self._sugerir_nombre_funcion(nodo.name)}'"
            )
        
        # Verificar type hints (solo funciones públicas)
        if self._es_funcion_publica(nodo):
            self._verificar_type_hints(nodo)
        
        # Verificar métodos privados
        if nodo.name.startswith('_') and not es_metodo_especial:
            self.nombres_privados.add(nodo.name)
        
        # Continuar visitando
        self.generic_visit(nodo)
    
    def visit_AsyncFunctionDef(self, nodo: ast.AsyncFunctionDef) -> None:
        """Verifica funciones asíncronas."""
        # Reutilizar la misma lógica que FunctionDef
        self.visit_FunctionDef(nodo)
    
    def visit_Assign(self, nodo: ast.Assign) -> None:
        """
        Verifica asignaciones (variables y constantes).
        
        - Nombre de constantes (MAYUSCULAS)
        """
        for destino in nodo.targets:
            if isinstance(destino, ast.Name):
                # Verificar si es constante (nivel módulo)
                if self._es_constante(destino.id):
                    if not self.PATRON_CONSTANTE.match(destino.id):
                        self._agregar_problema(
                            destino.lineno,
                            destino.col_offset,
                            Severidad.INFO,
                            "Nombre de constante inválido",
                            f"La constante '{destino.id}' debe estar en MAYUSCULAS",
                            f"Renombrar a '{destino.id.upper()}'"
                        )
        
        self.generic_visit(nodo)
    
    # ========================================================================
    # VERIFICACIONES ESPECÍFICAS
    # ========================================================================
    
    def _verificar_docstring(
        self,
        nodo: ast.AST,
        categoria: str,
        mensaje_faltante: str
    ) -> None:
        """
        Verifica la existencia de docstring.
        
        Args:
            nodo (ast.AST): Nodo a verificar.
            categoria (str): Categoría del problema.
            mensaje_faltante (str): Mensaje si falta docstring.
        """
        docstring = ast.get_docstring(nodo)
        if docstring is None:
            self._agregar_problema(
                nodo.lineno,
                nodo.col_offset,
                Severidad.ERROR,
                categoria,
                mensaje_faltante,
                "Agregar docstring con formato triple comillas \"\"\"\"\"\""
            )
        elif len(docstring.strip()) < 10:
            self._agregar_problema(
                nodo.lineno,
                nodo.col_offset,
                Severidad.WARNING,
                categoria,
                f"Docstring demasiado corto ({len(docstring)} caracteres)",
                "El docstring debe ser descriptivo (mínimo 10 caracteres)"
            )
    
    def _verificar_type_hints(self, nodo: ast.FunctionDef) -> None:
        """
        Verifica type hints en funciones.
        
        Args:
            nodo (ast.FunctionDef): Nodo de función.
        """
        # Verificar tipo de retorno
        if nodo.returns is None:
            self._agregar_problema(
                nodo.lineno,
                nodo.col_offset,
                Severidad.WARNING,
                "Type hint faltante",
                f"La función pública '{nodo.name}' no tiene type hint de retorno",
                "Agregar '-> Tipo' al final de la definición"
            )
        
        # Verificar argumentos
        for arg in nodo.args.args:
            if arg.annotation is None and arg.arg != 'self' and arg.arg != 'cls':
                self._agregar_problema(
                    arg.lineno if hasattr(arg, 'lineno') else nodo.lineno,
                    arg.col_offset if hasattr(arg, 'col_offset') else 0,
                    Severidad.WARNING,
                    "Type hint faltante",
                    f"El parámetro '{arg.arg}' no tiene type hint",
                    f"Agregar ': Tipo' después de '{arg.arg}'"
                )
        
        # Verificar tipo de self/cls
        for arg in nodo.args.args[:1]:
            if arg.arg in ('self', 'cls') and arg.annotation is not None:
                self._agregar_problema(
                    arg.lineno if hasattr(arg, 'lineno') else nodo.lineno,
                    arg.col_offset if hasattr(arg, 'col_offset') else 0,
                    Severidad.INFO,
                    "Type hint redundante",
                    f"El parámetro '{arg.arg}' no necesita type hint",
                    f"Eliminar ': Tipo' después de '{arg.arg}'"
                )
    
    # ========================================================================
    # MÉTODOS DE VALIDACIÓN
    # ========================================================================
    
    def _es_nombre_valido_clase(self, nombre: str) -> bool:
        """Verifica si un nombre de clase sigue CamelCase."""
        if nombre.startswith('_'):
            return True  # Clase privada
        return bool(self.PATRON_CLASE.match(nombre))
    
    def _es_nombre_valido_funcion(self, nombre: str) -> bool:
        """Verifica si un nombre de función sigue snake_case."""
        if nombre.startswith('_'):
            return True  # Función privada
        return bool(self.PATRON_FUNCION.match(nombre))
    
    def _es_funcion_publica(self, nodo: ast.FunctionDef) -> bool:
        """
        Determina si una función es pública.
        
        Args:
            nodo (ast.FunctionDef): Nodo de función.
        
        Returns:
            bool: True si es pública.
        """
        # Excluir métodos privados y especiales
        if nodo.name.startswith('_'):
            return False
        
        # Excluir funciones que son métodos especiales
        if nodo.name in self.METODOS_ESPECIALES:
            return False
        
        return True
    
    def _es_constante(self, nombre: str) -> bool:
        """
        Determina si un nombre es de constante (nivel módulo).
        
        Args:
            nombre (str): Nombre a verificar.
        
        Returns:
            bool: True si es constante.
        """
        # Excluir nombres privados
        if nombre.startswith('_'):
            return False
        
        # Excluir nombres en minúsculas (variables normales)
        if nombre.islower():
            return False
        
        # Si está todo en mayúsculas o tiene guión bajo, es constante
        return nombre.isupper() or '_' in nombre
    
    def _sugerir_nombre_clase(self, nombre: str) -> str:
        """Sugiere un nombre válido para una clase."""
        # Convertir snake_case a CamelCase
        partes = nombre.split('_')
        return ''.join(parte.capitalize() for parte in partes if parte)
    
    def _sugerir_nombre_funcion(self, nombre: str) -> str:
        """Sugiere un nombre válido para una función."""
        # Convertir CamelCase a snake_case
        nombre_convertido = re.sub(r'(?<=[a-z])([A-Z])', r'_\1', nombre)
        return nombre_convertido.lower()
    
    # ========================================================================
    # MÉTODOS AUXILIARES
    # ========================================================================
    
    def _agregar_problema(
        self,
        linea: int,
        columna: int,
        severidad: Severidad,
        categoria: str,
        mensaje: str,
        sugerencia: Optional[str] = None
    ) -> None:
        """
        Agrega un problema a la lista.
        
        Args:
            linea (int): Número de línea.
            columna (int): Número de columna.
            severidad (Severidad): Nivel de severidad.
            categoria (str): Categoría del problema.
            mensaje (str): Descripción del problema.
            sugerencia (Optional[str]): Sugerencia de corrección.
        """
        self.problemas.append(Problema(
            archivo=self.archivo,
            linea=linea,
            columna=columna,
            severidad=severidad,
            categoria=categoria,
            mensaje=mensaje,
            sugerencia=sugerencia
        ))


# ============================================================================
# VERIFICADOR DE ARCHIVOS
# ============================================================================

class VerificadorCalidad:
    """
    Verificador de calidad de código.
    
    Esta clase coordina el análisis de archivos Python y genera
    reportes de calidad.
    
    Attributes:
        directorio (Path): Directorio base para el análisis.
        excluir (List[str]): Patrones de exclusión.
        estadisticas (Estadisticas): Estadísticas del análisis.
    """
    
    # Patrones de archivos a excluir
    EXCLUIR_POR_DEFECTO = [
        'venv', 'env', '.venv', '.env',
        '__pycache__', '*.pyc',
        '.git', '.idea', '.vscode',
        'tests', 'test_*',
        'setup.py', 'conftest.py'
    ]
    
    def __init__(
        self,
        directorio: Optional[str] = None,
        excluir: Optional[List[str]] = None
    ) -> None:
        """
        Inicializa el verificador.
        
        Args:
            directorio (Optional[str]): Directorio a analizar.
            excluir (Optional[List[str]]): Patrones de exclusión.
        """
        self.directorio = Path(directorio or '.')
        self.excluir = excluir or self.EXCLUIR_POR_DEFECTO
        self.estadisticas = Estadisticas()
        self.todos_problemas: List[Problema] = []
    
    def verificar(self) -> List[Problema]:
        """
        Ejecuta la verificación en todos los archivos.
        
        Returns:
            List[Problema]: Lista de todos los problemas encontrados.
        """
        archivos = self._obtener_archivos_python()
        
        for archivo in archivos:
            problemas = self._verificar_archivo(archivo)
            self.todos_problemas.extend(problemas)
            self._actualizar_estadisticas(problemas, archivo)
        
        return self.todos_problemas
    
    def _obtener_archivos_python(self) -> List[Path]:
        """
        Obtiene todos los archivos Python en el directorio.
        
        Returns:
            List[Path]: Lista de rutas de archivos Python.
        """
        archivos: List[Path] = []
        
        for path in self.directorio.rglob('*.py'):
            if self._debe_excluir(path):
                continue
            archivos.append(path)
        
        return sorted(archivos)
    
    def _debe_excluir(self, path: Path) -> bool:
        """
        Determina si un archivo debe ser excluido.
        
        Args:
            path (Path): Ruta del archivo.
        
        Returns:
            bool: True si debe ser excluido.
        """
        # Verificar contra patrones de exclusión
        for patron in self.excluir:
            if patron.startswith('*'):
                if path.name.endswith(patron[1:]):
                    return True
            elif patron in str(path):
                return True
        return False
    
    def _verificar_archivo(self, archivo: Path) -> List[Problema]:
        """
        Verifica un archivo individual.
        
        Args:
            archivo (Path): Ruta del archivo.
        
        Returns:
            List[Problema]: Problemas encontrados en el archivo.
        """
        try:
            contenido = archivo.read_text(encoding='utf-8')
            arbol = ast.parse(contenido, filename=str(archivo))
            
            analizador = AnalizadorCodigo(str(archivo), contenido)
            return analizador.verificar(arbol)
            
        except SyntaxError as e:
            # Error de sintaxis
            return [Problema(
                archivo=str(archivo),
                linea=e.lineno or 0,
                columna=e.offset or 0,
                severidad=Severidad.ERROR,
                categoria="Error de sintaxis",
                mensaje=f"Error de sintaxis: {e.msg}",
                sugerencia="Revisar la sintaxis del archivo"
            )]
        except Exception as e:
            # Otros errores
            return [Problema(
                archivo=str(archivo),
                linea=0,
                columna=0,
                severidad=Severidad.ERROR,
                categoria="Error de análisis",
                mensaje=f"Error al analizar: {str(e)}",
                sugerencia="Verificar que el archivo sea válido"
            )]
    
    def _actualizar_estadisticas(
        self,
        problemas: List[Problema],
        archivo: Path
    ) -> None:
        """
        Actualiza las estadísticas con los problemas encontrados.
        
        Args:
            problemas (List[Problema]): Problemas encontrados.
            archivo (Path): Archivo analizado.
        """
        self.estadisticas.total_archivos += 1
        
        if not problemas:
            self.estadisticas.archivos_limpios += 1
        
        for problema in problemas:
            self.estadisticas.total_problemas += 1
            self.estadisticas.problemas_por_severidad[problema.severidad] += 1
            self.estadisticas.problemas_por_categoria[problema.categoria] = (
                self.estadisticas.problemas_por_categoria.get(problema.categoria, 0) + 1
            )
    
    def generar_reporte(self) -> str:
        """
        Genera un reporte completo del análisis.
        
        Returns:
            str: Reporte formateado.
        """
        lineas = []
        
        # Encabezado
        lineas.append("=" * 80)
        lineas.append("REPORTE DE VERIFICACIÓN DE CALIDAD DE CÓDIGO")
        lineas.append("=" * 80)
        lineas.append("")
        
        # Estadísticas
        lineas.append("📊 ESTADÍSTICAS:")
        lineas.append("-" * 40)
        lineas.append(f"Total de archivos: {self.estadisticas.total_archivos}")
        lineas.append(f"Archivos sin problemas: {self.estadisticas.archivos_limpios}")
        lineas.append(f"Total de problemas: {self.estadisticas.total_problemas}")
        lineas.append("")
        
        # Desglose por severidad
        lineas.append("📈 POR SEVERIDAD:")
        for severidad in Severidad:
            cantidad = self.estadisticas.problemas_por_severidad[severidad]
            if cantidad > 0:
                emoji = {
                    Severidad.ERROR: "❌",
                    Severidad.WARNING: "⚠️",
                    Severidad.INFO: "ℹ️"
                }.get(severidad, "•")
                lineas.append(f"  {emoji} {severidad.value}: {cantidad}")
        lineas.append("")
        
        # Desglose por categoría
        if self.estadisticas.problemas_por_categoria:
            lineas.append("📂 POR CATEGORÍA:")
            for categoria, cantidad in sorted(
                self.estadisticas.problemas_por_categoria.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                lineas.append(f"  • {categoria}: {cantidad}")
            lineas.append("")
        
        # Problemas detallados
        if self.todos_problemas:
            lineas.append("🔍 PROBLEMAS DETALLADOS:")
            lineas.append("-" * 40)
            lineas.append("")
            
            # Agrupar por archivo
            por_archivo: Dict[str, List[Problema]] = {}
            for problema in self.todos_problemas:
                por_archivo.setdefault(problema.archivo, []).append(problema)
            
            for archivo, problemas in sorted(por_archivo.items()):
                lineas.append(f"📄 {archivo}")
                
                # Priorizar por severidad
                problemas.sort(key=lambda p: (
                    0 if p.severidad == Severidad.ERROR else
                    1 if p.severidad == Severidad.WARNING else 2,
                    p.linea
                ))
                
                for problema in problemas:
                    lineas.append(f"  {problema}")
                
                lineas.append("")
        
        # Resumen
        lineas.append("=" * 80)
        if self.estadisticas.total_problemas == 0:
            lineas.append("✅ ¡FELICITACIONES! Todos los archivos cumplen con los estándares.")
        else:
            lineas.append(f"⚠️ Se encontraron {self.estadisticas.total_problemas} problemas.")
            lineas.append(f"💡 Revisa los problemas detallados para corregirlos.")
        lineas.append("=" * 80)
        
        return '\n'.join(lineas)


# ============================================================================
# INTERFAZ DE LÍNEA DE COMANDOS
# ============================================================================

def configurar_argumentos() -> argparse.ArgumentParser:
    """
    Configura el parser de argumentos de línea de comandos.
    
    Returns:
        argparse.ArgumentParser: Parser configurado.
    """
    parser = argparse.ArgumentParser(
        description='Verificador automático de calidad de código Python',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EJEMPLOS DE USO:
  %(prog)s                    # Verifica el directorio actual
  %(prog)s src/               # Verifica el directorio src/
  %(prog)s archivo.py         # Verifica un archivo específico
  %(prog)s --excluir tests/   # Excluye el directorio tests/
  %(prog)s --salida reporte.txt  # Guarda el reporte en un archivo
  
CÓDIGOS DE SALIDA:
  0 - Todos los archivos cumplen con los estándares
  1 - Se encontraron problemas
  2 - Error en la ejecución
        """
    )
    
    parser.add_argument(
        'ruta',
        nargs='?',
        default='.',
        help='Archivo o directorio a verificar (por defecto: directorio actual)'
    )
    
    parser.add_argument(
        '--excluir',
        action='append',
        help='Patrón de exclusión (puede repetirse)'
    )
    
    parser.add_argument(
        '--salida',
        '-o',
        help='Archivo de salida para el reporte'
    )
    
    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        help='Modo silencioso (solo estadísticas)'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Modo estricto (info y warnings son errores)'
    )
    
    parser.add_argument(
        '--solo-error',
        action='store_true',
        help='Solo muestra errores (ignora warnings e info)'
    )
    
    return parser


def main() -> int:
    """
    Función principal del script.
    
    Returns:
        int: Código de salida (0 = éxito, 1 = problemas, 2 = error)
    """
    parser = configurar_argumentos()
    args = parser.parse_args()
    
    try:
        # Configurar verificador
        verificador = VerificadorCalidad(
            directorio=args.ruta,
            excluir=args.excluir
        )
        
        # Ejecutar verificación
        print("🔍 Analizando código...")
        problemas = verificador.verificar()
        
        # Generar reporte
        reporte = verificador.generar_reporte()
        
        # Filtrar según opciones
        if args.solo_error:
            # Solo mostrar errores
            lineas_filtradas = []
            mostrar = False
            for linea in reporte.split('\n'):
                if '❌' in linea:
                    mostrar = True
                elif '⚠️' in linea or 'ℹ️' in linea:
                    mostrar = False
                elif mostrar:
                    lineas_filtradas.append(linea)
            reporte = '\n'.join(lineas_filtradas)
        
        # Mostrar u guardar reporte
        if args.salida:
            Path(args.salida).write_text(reporte, encoding='utf-8')
            print(f"✅ Reporte guardado en: {args.salida}")
        else:
            print(reporte)
        
        # Determinar código de salida
        if verificador.estadisticas.total_problemas == 0:
            return 0
        elif args.strict:
            # En modo estricto, cualquier problema es error
            return 1
        elif verificador.estadisticas.problemas_por_severidad[Severidad.ERROR] > 0:
            # Solo errores causan fallo
            return 1
        else:
            # Warnings e info no causan fallo
            return 0
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 2


# ============================================================================
# EJECUCIÓN DEL SCRIPT
# ============================================================================

if __name__ == "__main__":
    sys.exit(main())