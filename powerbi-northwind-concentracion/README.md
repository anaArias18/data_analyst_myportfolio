# 📊 Concentración de ventas por cliente y país (Power BI)

Dashboard de Power BI que responde: **¿qué tan concentradas están las ventas en pocos clientes, y de qué países vienen?**

![Resumen](img/resumen.png)
![Detalle de país](img/detalle_pais.png)

## 📂 Datos

Base tipo Northwind simplificada y en español, con **datos sintéticos generados para práctica**: 8 categorías, 40 productos, 20 clientes de 7 países, 120 pedidos y 361 líneas de pedido, del 2 de enero al 29 de agosto de 2026. Como los datos son sintéticos, los hallazgos ilustran el método de análisis y no describen un negocio real.

## 🧱 Modelo de datos (esquema en estrella)

- **Tabla de hechos `Ventas`:** una fila por línea de pedido (granularidad más fina), con la fecha y el cliente traídos del encabezado del pedido mediante un Merge en Power Query.
- **Dimensiones:** `Clientes`, `Productos` (con la categoría aplanada) y `Calendario`.
- Relaciones de uno a varios, con filtro de la dimensión hacia los hechos.
- Los totales se validaron contra una consulta SQL sobre la misma base (₡51,283,849.07).

## 🧮 Medidas DAX principales

| Medida | Qué hace |
|---|---|
| `Total Ventas` | Suma del importe (`Cantidad × PrecioUnitario`) |
| `Clientes Activos` | Cantidad de clientes distintos con ventas |
| `Ranking Cliente` | Posición global de cada cliente, con `RANKX` y `ALL(Clientes)` |
| `Participacion Top 3` | Porcentaje de las ventas que concentran los 3 mejores clientes |
| `Porcentaje Acumulado` | Ventas acumuladas por cliente, para la curva de Pareto |

## 🔎 Hallazgos

1. **Concentración moderada.** Los 3 mejores clientes aportan el **27.4%** de las ventas, casi el doble del 15% que tendrían en un reparto parejo. Hacen falta 7 de 20 clientes para pasar el 50%, y 14 de 20 (el 70%) para llegar al 82.5%. Está lejos de la regla 80/20, en la que un 20% de los clientes aportaría el 80%.
2. **Riesgo por cliente individual acotado.** El mayor cliente, Mercado Andino, aporta el 10.1%: perderlo restaría un 10% de las ventas.
3. **La dependencia geográfica es en realidad dependencia de tres compradores.** Chile aporta el 30% de las ventas con solo 4 clientes, y los 3 mejores clientes de toda la cartera son chilenos.
4. **Junio fue el mejor mes (₡10.36M) sin ser el de más pedidos.** Marzo tuvo más pedidos (21), pero junio dejó un ticket por pedido un 23% mayor (₡517,778 contra ₡419,818).

## 🧩 Decisiones y aprendizajes

- `ALL(Clientes)` en lugar de `ALL(Clientes[NombreCliente])`: con la columna sola, el filtro de país seguía activo y el ranking cambiaba. Con la tabla entera el indicador es global.
- Verificar los filtros activos antes de leer un número: una barra seleccionada hacía que las tarjetas mostraran solo Chile.
- Una medida de porcentaje se valida con la lógica: una participación nunca supera el 100%.

## 🛠️ Herramientas

Power BI Desktop, Power Query, DAX, SQL (validación) y Git.

## 📁 Archivos

- `northwind_concentracion.pbix`: archivo editable del dashboard.
- `data/`: los 5 CSV de la base.
- `img/`: capturas del dashboard.