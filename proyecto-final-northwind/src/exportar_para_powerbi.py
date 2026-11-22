"""Exporta el warehouse a CSV para Power BI (que no tiene conector nativo de SQLite)."""
import argparse
import os
import sqlite3
import sys

import numpy as np
import pandas as pd

TABLAS = ["dim_cliente", "dim_producto", "dim_fecha", "fact_ventas_lineas"]


def aporte_palancas(con):
    """Peso de cada palanca en la variación mensual del ingreso (descomposición en logaritmos)."""
    m = pd.read_sql("""
        SELECT f.anio_mes AS mes, COUNT(DISTINCT v.pedido_id) AS pedidos, COUNT(*) AS lineas,
               SUM(v.cantidad) AS unidades, SUM(v.monto_linea) AS ingreso
        FROM fact_ventas_lineas v JOIN dim_fecha f ON v.fecha_key = f.fecha_key
        GROUP BY f.anio_mes""", con)
    m["lineas_x_pedido"] = m["lineas"] / m["pedidos"]
    m["unidades_x_linea"] = m["unidades"] / m["lineas"]
    m["precio_x_unidad"] = m["ingreso"] / m["unidades"]
    palancas = ["pedidos", "lineas_x_pedido", "unidades_x_linea", "precio_x_unidad"]
    logs = np.log(m[palancas + ["ingreso"]])
    pesos = [logs[p].cov(logs["ingreso"]) / logs["ingreso"].var() * 100 for p in palancas]
    nombres = ["Pedidos", "Líneas por pedido", "Unidades por línea", "Precio por unidad (mezcla)"]
    return pd.DataFrame({"palanca": nombres, "aporte_pct": np.round(pesos, 1)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/warehouse.db")
    ap.add_argument("--salida", default="powerbi/datos")
    a = ap.parse_args()
    if not os.path.exists(a.db):
        sys.exit(f"No encuentro el warehouse: {a.db}. Corré primero src/pipeline.py")
    os.makedirs(a.salida, exist_ok=True)
    con = sqlite3.connect(a.db)
    for t in TABLAS:
        df = pd.read_sql_query(f"SELECT * FROM {t}", con)
        df.to_csv(os.path.join(a.salida, f"{t}.csv"), index=False, encoding="utf-8-sig")
        print(f"{t}.csv: {len(df)} filas")
    ap_df = aporte_palancas(con)
    ap_df.to_csv(os.path.join(a.salida, "aporte_palancas.csv"), index=False, encoding="utf-8-sig")
    print(f"aporte_palancas.csv: {len(ap_df)} filas")
    con.close()


if __name__ == "__main__":
    main()