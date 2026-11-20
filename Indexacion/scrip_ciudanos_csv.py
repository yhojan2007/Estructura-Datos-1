"""Genera un CSV con N ciudadanos de Bolivia (datos ficticios, CI únicos).

Uso:  python generar_csv.py            -> 2,000,000 filas
      python generar_csv.py 5000000    -> 5,000,000 filas
"""
import csv
import random
import sys
import time
from datetime import date, timedelta

N = int(sys.argv[1]) if len(sys.argv) > 1 else 11_000_000
ARCHIVO = "ciudadanos.csv"

NOMBRES = ["Juan", "María", "Luis", "Ana", "Carlos", "Rosa", "José", "Elena",
           "Pedro", "Lucía", "Miguel", "Carmen", "Jorge", "Sofía", "Daniel"]
APELLIDOS = ["Quispe", "Mamani", "Pérez", "Rojas", "Vaca", "Flores", "Choque",
             "Condori", "Gutiérrez", "Fernández", "Copa", "Huanca", "Aguilar"]
DEPARTAMENTOS = ["La Paz", "Cochabamba", "Santa Cruz", "Oruro", "Potosí",
                 "Chuquisaca", "Tarija", "Beni", "Pando"]

t0 = time.perf_counter()

# CIs únicos (como en un índice único real); se mezclan para que no estén ordenados
cis = random.sample(range(1_000_000, 14_000_000), N)

base = date(1940, 1, 1)
dias = (date(2008, 12, 31) - base).days

with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["ci", "nombres", "apellido_paterno", "apellido_materno",
                "fecha_nacimiento", "departamento"])
    for i, ci in enumerate(cis, 1):
        w.writerow([
            ci,
            random.choice(NOMBRES),
            random.choice(APELLIDOS),
            random.choice(APELLIDOS),
            (base + timedelta(days=random.randint(0, dias))).isoformat(),
            random.choice(DEPARTAMENTOS),
        ])
        if i % 500_000 == 0:
            print(f"  {i:,} filas escritas...")

print(f"Listo: {N:,} filas en '{ARCHIVO}' ({time.perf_counter() - t0:.2f} s)")