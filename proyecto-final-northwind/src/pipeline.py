"""Pipeline ETL: northwind.db (origen) -> warehouse.db (modelo en estrella)."""
import argparse
import logging
import os
import sqlite3
import sys

import pandas as pd

log = logging.getLogger("pipeline")


class DataQualityError(Exception):
    """Se lanza cuando los datos no pasan las validaciones."""


RENOMBRAR = {
    "Categorias": {"CategoriaID": "categoria_id", "NombreCategoria": "nombre_categoria", "Descripcion": "descripcion"},
    "Clientes": {"ClienteID": "cliente_id", "NombreCliente": "nombre_cliente", "Pais": "pais", "Ciudad": "ciudad"},
    "DetallesPedido": {"DetalleID": "detalle_id", "PedidoID": "pedido_id", "ProductoID": "producto_id", "Cantidad": "cantidad"},
    "Pedidos": {"PedidoID": "pedido_id", "ClienteID": "cliente_id", "FechaPedido": "fecha_pedido", "Pais": "pais"},
    "Productos": {"ProductoID": "producto_id", "NombreProducto": "nombre_producto", "CategoriaID": "categoria_id",
                  "PrecioUnitario": "precio_unitario", "UnidadesEnStock": "unidades_en_stock"},
}
NOMBRES = {"Categorias": "categorias", "Clientes": "clientes", "DetallesPedido": "detalles",
           "Pedidos": "pedidos", "Productos": "productos"}
MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
         8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
DIAS = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}


# ---------- EXTRACT + STANDARDIZE ----------
def extract(origen):
    if not os.path.exists(origen):  # sqlite3.connect crearía una base vacía en silencio
        raise FileNotFoundError(f"No encuentro la base de origen: {origen}")
    con = sqlite3.connect(origen)
    t = {}
    for tabla, nuevo in NOMBRES.items():
        df = pd.read_sql_query(f'SELECT * FROM "{tabla}"', con).rename(columns=RENOMBRAR[tabla])
        t[nuevo] = df
        log.info("Extract: %s = %d filas", tabla, len(df))
    con.close()
    return t


# ---------- VALIDATE ----------
def validate(t):
    ped, det, pro, cli, cat = t["pedidos"], t["detalles"], t["productos"], t["clientes"], t["categorias"]
    e = {}
    e["nulos_total"] = int(sum(df.isna().sum().sum() for df in t.values()))
    e["detalle_id_duplicados"] = int(det["detalle_id"].duplicated().sum())
    e["pedido_id_duplicados"] = int(ped["pedido_id"].duplicated().sum())
    e["producto_id_duplicados"] = int(pro["producto_id"].duplicated().sum())
    e["cantidad_menor_o_igual_0"] = int((det["cantidad"] <= 0).sum())
    e["precio_menor_o_igual_0"] = int((pro["precio_unitario"] <= 0).sum())
    e["fechas_invalidas"] = int(pd.to_datetime(ped["fecha_pedido"], format="%Y-%m-%d", errors="coerce").isna().sum())
    e["detalles_sin_pedido"] = int((~det["pedido_id"].isin(ped["pedido_id"])).sum())
    e["detalles_sin_producto"] = int((~det["producto_id"].isin(pro["producto_id"])).sum())
    e["pedidos_sin_cliente"] = int((~ped["cliente_id"].isin(cli["cliente_id"])).sum())
    e["productos_sin_categoria"] = int((~pro["categoria_id"].isin(cat["categoria_id"])).sum())
    e["pedidos_sin_lineas"] = int((~ped["pedido_id"].isin(det["pedido_id"])).sum())

    avisos = {}  # política: se REPORTAN y el pipeline sigue (no son datos imposibles)
    m = ped.merge(cli[["cliente_id", "pais"]], on="cliente_id", how="left", suffixes=("_pedido", "_cliente"))
    avisos["pais_pedido_distinto_de_pais_cliente"] = int((m["pais_pedido"] != m["pais_cliente"]).sum())

    malos = {k: v for k, v in e.items() if v > 0}
    if malos:
        raise DataQualityError(f"Validación fallida: {malos}")
    log.info("Validate: %d chequeos de error, 0 problemas", len(e))
    for k, v in avisos.items():
        (log.warning if v > 0 else log.info)("Aviso %s: %d", k, v)


# ---------- TRANSFORM ----------
def transform(t):
    ped, det, pro, cli, cat = t["pedidos"], t["detalles"], t["productos"], t["clientes"], t["categorias"]

    dim_cliente = cli.rename(columns={"cliente_id": "cliente_key"})[["cliente_key", "nombre_cliente", "pais", "ciudad"]]

    dim_producto = (pro.merge(cat[["categoria_id", "nombre_categoria"]], on="categoria_id", how="left")
                       .rename(columns={"producto_id": "producto_key", "precio_unitario": "precio_lista"})
                       [["producto_key", "nombre_producto", "categoria_id", "nombre_categoria", "precio_lista"]])

    fechas_pedido = pd.to_datetime(ped["fecha_pedido"], format="%Y-%m-%d")
    cal = pd.DataFrame({"fecha": pd.date_range(fechas_pedido.min(), fechas_pedido.max(), freq="D")})
    cal["fecha_key"] = cal["fecha"].dt.strftime("%Y%m%d").astype(int)
    cal["anio"] = cal["fecha"].dt.year
    cal["trimestre"] = cal["fecha"].dt.quarter
    cal["mes"] = cal["fecha"].dt.month
    cal["anio_mes"] = cal["fecha"].dt.strftime("%Y-%m")
    cal["nombre_mes"] = cal["mes"].map(MESES)
    cal["dia_semana"] = cal["fecha"].dt.dayofweek.map(DIAS)
    cal["fecha"] = cal["fecha"].dt.strftime("%Y-%m-%d")
    dim_fecha = cal[["fecha_key", "fecha", "anio", "trimestre", "mes", "anio_mes", "nombre_mes", "dia_semana"]]

    p = ped.rename(columns={"pais": "pais_pedido"}).copy()
    p["fecha_key"] = pd.to_datetime(p["fecha_pedido"], format="%Y-%m-%d").dt.strftime("%Y%m%d").astype(int)
    f = (det.merge(p[["pedido_id", "cliente_id", "fecha_key", "pais_pedido"]], on="pedido_id", how="left")
            .merge(pro[["producto_id", "precio_unitario"]], on="producto_id", how="left"))
    if len(f) != len(det):
        raise DataQualityError(f"Un merge cambió el número de filas: {len(det)} -> {len(f)}")
    f["monto_linea"] = f["cantidad"] * f["precio_unitario"]
    fact = (f.rename(columns={"cliente_id": "cliente_key", "producto_id": "producto_key"})
             [["detalle_id", "pedido_id", "fecha_key", "cliente_key", "producto_key", "pais_pedido",
               "cantidad", "precio_unitario", "monto_linea"]])

    tablas = {"dim_cliente": dim_cliente, "dim_producto": dim_producto, "dim_fecha": dim_fecha,
              "fact_ventas_lineas": fact}
    log.info("Transform: " + ", ".join(f"{k}={len(v)}" for k, v in tablas.items()))
    return tablas


# ---------- LOAD ----------
SCHEMA = """
CREATE TABLE dim_cliente  (cliente_key INTEGER PRIMARY KEY, nombre_cliente TEXT NOT NULL,
                           pais TEXT NOT NULL, ciudad TEXT NOT NULL);
CREATE TABLE dim_producto (producto_key INTEGER PRIMARY KEY, nombre_producto TEXT NOT NULL,
                           categoria_id INTEGER NOT NULL, nombre_categoria TEXT NOT NULL, precio_lista REAL NOT NULL);
CREATE TABLE dim_fecha    (fecha_key INTEGER PRIMARY KEY, fecha TEXT NOT NULL, anio INTEGER, trimestre INTEGER,
                           mes INTEGER, anio_mes TEXT, nombre_mes TEXT, dia_semana TEXT);
CREATE TABLE fact_ventas_lineas (
    detalle_id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL,
    fecha_key INTEGER NOT NULL REFERENCES dim_fecha(fecha_key),
    cliente_key INTEGER NOT NULL REFERENCES dim_cliente(cliente_key),
    producto_key INTEGER NOT NULL REFERENCES dim_producto(producto_key),
    pais_pedido TEXT,
    cantidad INTEGER NOT NULL, precio_unitario REAL NOT NULL, monto_linea REAL NOT NULL
);
"""


def load(tablas, db_path):
    """Carga en un archivo temporal y lo reemplaza al final: si falla, el warehouse anterior queda intacto."""
    tmp = db_path + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    con = sqlite3.connect(tmp)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(SCHEMA)
        for nombre, tabla in tablas.items():
            tabla.to_sql(nombre, con, if_exists="append", index=False)
        con.commit()
    except Exception:
        con.close()
        os.remove(tmp)
        raise
    con.close()
    os.replace(tmp, db_path)
    log.info("Load: warehouse escrito en %s", db_path)


# ---------- RECONCILE (contra el ORIGEN, calculado con SQL independiente) ----------
def reconcile(origen, db_path):
    o = sqlite3.connect(origen)
    n_det = o.execute("SELECT COUNT(*) FROM DetallesPedido").fetchone()[0]
    n_ped = o.execute("SELECT COUNT(*) FROM Pedidos").fetchone()[0]
    ingreso_origen = o.execute("""SELECT SUM(d.Cantidad * p.PrecioUnitario)
                                  FROM DetallesPedido d JOIN Productos p ON d.ProductoID = p.ProductoID""").fetchone()[0]
    o.close()
    w = sqlite3.connect(db_path)
    n_fact, ingreso_wh, ped_wh = w.execute(
        "SELECT COUNT(*), SUM(monto_linea), COUNT(DISTINCT pedido_id) FROM fact_ventas_lineas").fetchone()
    fk = w.execute("PRAGMA foreign_key_check").fetchall()
    w.close()
    if n_fact != n_det:
        raise DataQualityError(f"Líneas: origen {n_det} vs warehouse {n_fact}")
    if ped_wh != n_ped:
        raise DataQualityError(f"Pedidos: origen {n_ped} vs warehouse {ped_wh}")
    if abs(ingreso_wh - ingreso_origen) > 0.01:
        raise DataQualityError(f"Ingreso: origen {ingreso_origen:,.2f} vs warehouse {ingreso_wh:,.2f}")
    if fk:
        raise DataQualityError(f"Llaves foráneas rotas: {fk}")
    log.info("Reconcile: %d líneas, %d pedidos, ingreso ₡%s, ticket promedio ₡%s, 0 FK rotas",
             n_fact, ped_wh, f"{ingreso_wh:,.2f}", f"{ingreso_wh / ped_wh:,.2f}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--origen", default="data/northwind.db")
    ap.add_argument("--db", default="data/warehouse.db")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler("pipeline.log", encoding="utf-8")])
    try:
        t = extract(a.origen)
        validate(t)
        tablas = transform(t)
        load(tablas, a.db)
        reconcile(a.origen, a.db)
        log.info("Pipeline terminado OK")
        return 0
    except DataQualityError as e:
        log.error("DATOS RECHAZADOS: %s", e)
        return 1
    except Exception:
        log.exception("Error inesperado")
        return 2


if __name__ == "__main__":
    sys.exit(main())