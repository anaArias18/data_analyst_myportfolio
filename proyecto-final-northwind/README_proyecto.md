# ¿Qué explica la variación mensual del ingreso? Pipeline ETL, modelo en estrella, SQL, estadística y dashboard

> **Aviso:** los datos de Northwind simplificado son **sintéticos**, generados para práctica. Los hallazgos no describen un negocio real; el objetivo es demostrar el proceso analítico completo, de punta a punta.

## Pregunta de negocio
¿Qué explica la variación mensual del ingreso de 2026: más pedidos, pedidos más grandes o un cambio en la mezcla de productos?

## Resumen de hallazgos
- El ingreso se descompone como **pedidos × líneas por pedido × unidades por línea × precio por unidad**. En los 8 meses analizados, los **pedidos** explican el 52.5% de la variación del ingreso, la **mezcla de productos** (precio por unidad) el 17.3%, las líneas por pedido el 15.3% y las unidades por línea el 15.0%.
- **Junio** es el mejor mes (₡10,355,550.62) sin ser el de más pedidos (marzo: 21; junio: 20). Su desvío sobre el promedio se debe en 56.8% a más pedidos y en 35.0% a la mezcla de productos (precio por unidad de ₡15,456.05, el más alto del período).
- **Cautela estadística:** la variación mensual del número de pedidos es compatible con el azar (χ² = 6.667, p = 0.46), y el ticket de junio no es significativamente mayor que el del resto (Welch p = 0.167).
- **Chile** concentra el 30.0% del ingreso; sus 3 mejores clientes son chilenos.

## Datos
`northwind.db` con 5 tablas: Categorias (8), Productos (40), Clientes (20, en 7 países), Pedidos (120, del 2/1/2026 al 29/8/2026) y DetallesPedido (361 líneas). Ingreso total: **₡51,283,849.07**; ticket promedio: **₡427,365.41**.

## Arquitectura
```
northwind.db → extract → validate → transform → load (archivo temporal + os.replace) → reconcile → warehouse.db
                              ↓ (si falla)
                      DataQualityError: se detiene sin tocar el warehouse
```

| Etapa | Qué hace |
|---|---|
| `extract` | Lee las 5 tablas del origen (falla con un error claro si el archivo no existe) |
| `validate` | 12 chequeos que detienen el pipeline (nulos, duplicados, rangos, fechas, huérfanos) y avisos que solo se reportan |
| `transform` | Construye 3 dimensiones y la tabla de hechos |
| `load` | Escribe en un archivo temporal y lo reemplaza al final: si algo falla, el warehouse anterior queda intacto |
| `reconcile` | Compara líneas, pedidos e ingreso contra el origen con SQL independiente y revisa las llaves foráneas |

**Política de calidad:** los datos imposibles o que alterarían las cifras **frenan** el pipeline; lo discutible (por ejemplo, el país del pedido distinto al del cliente) se **reporta** y sigue. Con los datos reales hay 0 problemas.

## Modelo (esquema en estrella)
- **Grano:** una fila de `fact_ventas_lineas` = una línea de pedido (`detalle_id`, PK).
- **Hechos:** `fact_ventas_lineas` (361): cantidad, precio unitario y monto de la línea.
- **Dimensiones:** `dim_cliente` (20), `dim_producto` (40, con su categoría), `dim_fecha` (240 días).
- El precio vive en `Productos` (uno por producto) y se copia a cada línea en la carga. Como no hay historial de precios, el precio por unidad solo cambia por la **mezcla** de productos.

## Análisis
- **SQL** (`sql/consultas.sql`): resumen mensual con las 4 palancas, ranking, variación contra el mes anterior y acumulado (`RANK`, `LAG`, `SUM() OVER`), categoría líder por mes (`ROW_NUMBER` con `PARTITION BY`), top de productos y concentración por país.
- **Pandas y estadística** (`notebooks/analisis.ipynb`): descomposición en logaritmos, prueba de dispersión contra el azar, prueba t de Welch con intervalo de confianza y tamaño del efecto, y análisis de la mezcla de productos.

## Dashboard (Power BI)
El archivo `.pbix` es binario, por eso se documenta con capturas.

| Página | Mensaje |
|---|---|
| ![Resumen](powerbi/img/01_resumen.png) | Junio fue el mejor mes del período |
| ![Palancas](powerbi/img/02_palancas.png) | Los pedidos pesan más, y la mezcla de productos es la segunda palanca |
| ![Mezcla](powerbi/img/03_mezcla.png) | Qué categorías y productos sostienen el ingreso |
| ![Clientes y países](powerbi/img/04_clientes_paises.png) | Chile concentra el 30% del ingreso |

## Cómo reproducirlo (Windows, PowerShell)
```powershell
python -m venv data-analyst-env
data-analyst-env\Scripts\Activate.ps1
pip install pandas scipy matplotlib jupyter
python src\pipeline.py          # genera data\warehouse.db
python src\exportar_csv.py      # CSV para Power BI en data\export
```
Cerrar DB Browser for SQLite antes de correr el pipeline (en Windows bloquea el archivo).

## Estructura del repositorio
```
proyecto-final-northwind/
├── README.md
├── data/northwind.db          (fuente sintética; el warehouse se genera con el script)
├── src/pipeline.py
├── src/exportar_csv.py
├── sql/consultas.sql
├── notebooks/analisis.ipynb
└── powerbi/ (dashboard .pbix y capturas en img/)
```

## Limitaciones
- **Datos sintéticos** de un solo año (2/1/2026 al 29/8/2026), sin comparación interanual.
- Hay pedidos en solo 91 de los 240 días y ≈15 pedidos por mes: las diferencias mensuales pueden ser ruido, así que no se afirman causas firmes.
- Junio se eligió después de ver que era el mes más alto (análisis post hoc), lo que favorece encontrar diferencias aparentes.
- La descomposición es contable: describe cuánto pesa cada palanca, no sus causas.
- Cada producto tiene un único precio, por lo que no se puede atribuir cambios del ingreso a variaciones de precio.
- Carga completa (no incremental) y ejecución manual.

## Próximos pasos
Pruebas automatizadas con `pytest`, carga incremental, programar la ejecución y repetir el análisis con un dataset real.
