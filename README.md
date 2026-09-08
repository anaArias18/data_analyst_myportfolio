# 📊 Portafolio de Data Analyst

Repositorio de práctica y proyectos del plan de aprendizaje de 13 semanas para convertirme en Data Analyst Junior. Documento acá mi avance semana a semana, con código, archivos y notas de lo aprendido.

---

## 🛠️ Setup (Semana 0)

- ✅ Python 3.14.6 instalado y funcionando
- ✅ Entorno virtual (venv) configurado para aislar librerías del proyecto
- ✅ Visual Studio Code como editor principal
- ✅ Git + GitHub configurados y conectados
- ✅ Power BI Desktop instalado
- ✅ Repositorio de portafolio creado y clonado localmente

---

## 📅 Semana 1: Fundamentos y Excel Avanzado

**Estado: 🔄 En progreso (Día 1 al 5 completos)**

### Día 1 — Interfaz y referencias
- Repaso de conceptos base: dataset, variable, registro, tipo de dato
- Referencias relativas vs. absolutas (`$` para anclar celdas)
- Tabla de ventas ficticia de 50 filas, con formato de tabla (`Ctrl+T`)
- Fórmula de conversión de colones a dólares con referencia absoluta

### Día 2 — Fórmulas condicionales
- `SUMAR.SI` — suma valores que cumplen una condición
- `CONTAR.SI` — cuenta ocurrencias que cumplen una condición
- `SI` — lógica condicional (prueba lógica, valor si verdadero, valor si falso)
- Aplicadas sobre la tabla de ventas: total por región, conteo por vendedor, clasificación Alta/Baja

### Día 3 — Búsquedas (XLOOKUP y BUSCARV)
- `XLOOKUP` / `BUSCARX` — busca un valor y trae un dato relacionado de otra tabla, en cualquier dirección
- `BUSCARV` — versión clásica, busca solo hacia la derecha, requiere número de columna
- Tabla de productos (Producto, Precio, Categoría) conectada a la tabla de ventas
- Detecté y corregí un bug real: dos celdas de la columna `SI` con referencias desalineadas por una interrupción en el arrastre del controlador de relleno
- Extra: usé `UNIQUE()` para extraer lista de vendedores sin duplicados

### Día 4-5 — Tablas dinámicas y Power Query
**Tablas dinámicas:**
- 4 pivots sobre la tabla de ventas: total por región, promedio por producto, conteo por vendedor/mes, promedio de venta por vendedor
- Gráfico dinámico de columnas comparando promedio de venta por vendedor

**Power Query:**
- Importé un dataset real de 1,000 filas (ventas internacionales) desde CSV
- Verifiqué tipos de datos (fechas y números ya venían correctos)
- Verifiqué duplicados por `Order ID` (no se encontraron — dataset ya venía curado)
- Eliminé una columna innecesaria para el análisis
- Aprendí que Power Query no modifica el archivo original: cada limpieza queda como un "paso" reversible

---

## 💡 Habilidades cubiertas hasta ahora

- Excel: referencias relativas/absolutas, SUMAR.SI, CONTAR.SI, SI, XLOOKUP, BUSCARV
- Tablas dinámicas y gráficos dinámicos
- Power Query: importación y limpieza de datos
- Git: `add`, `commit`, `push`, control de versiones básico
- Debugging: identificar y corregir errores de fórmulas en datos reales

---

## 📂 Archivos en este repositorio


---

## 🎯 Próximos pasos

- Semana 1 (cierre): mini-proyecto integrador (sábado) + repaso (domingo)
- Semana 2: Power Query avanzado
- Semanas 3-4: SQL intensivo

____________________________

## Semana 2

### Dia 1: XLOOKUP vs. Merge (Power Query)

XLOOKUP es una fórmula que trabaja fila por fila dentro de una hoja de Excel — busca un valor y trae un dato relacionado desde otra tabla. En esencia, siempre se comporta como una "Externa izquierda": conserva todas mis filas actuales y trae lo que coincida.

Merge, en cambio, funciona dentro de Power Query y combina tablas completas entre sí, no fila por fila. Su ventaja principal es que da control real sobre cómo tratar los datos que no coinciden entre ambas tablas — con tipos como Externa izquierda, Interna o Externa derecha, cada uno responde una pregunta de negocio distinta. Además, al estar dentro de Power Query, la combinación se recalcula automáticamente si los datos originales cambian, sin necesidad de volver a arrastrar ninguna fórmula.
Con 60 ventas y un producto ('Audífonos') fuera de catálogo: Externa izquierda me dio 60 filas con nulls, Interna me dio 49 filas sin nulls

### Día 2 (Martes) — Anexar consultas (Append)

- `Append` apila dos tablas con la misma estructura de columnas, una debajo de otra — a diferencia de `Merge`, que combina tablas agregando columnas nuevas
- Junté ventas de "enero" (60 filas) con ventas de "febrero" (20 filas) → resultado: 69 filas
- **Aprendizaje clave sobre orden de operaciones:** como hice el Merge (con la tabla de productos) *antes* del Append, las 20 filas nuevas de febrero quedaron sin Precio/Categoría (null), porque nunca pasaron por ese cruce. Si hubiera anexado primero y combinado después, todas las filas habrían quedado completas.

### Día 3 (Miércoles) — Columna condicional y Agrupar por

- **Columna condicional:** el equivalente visual (sin fórmula) de `SI()` — clasifiqué cada venta como "Alta" o "Baja" según si el Monto supera 50,000
- **Agrupar por:** el equivalente de una tabla dinámica o `GROUP BY`, pero generado dentro de Power Query como una tabla nueva, no interactiva
- Usé **Referencia de consulta** para mantener dos versiones de mis datos sin duplicar trabajo: una con el detalle completo (con la columna condicional) y otra resumida (agrupada por vendedor)
- Resultado del agrupado por Vendedor (Recuento de ventas):

| Vendedor | Cantidad de ventas |
|---|---|
| maria | 21 |
| juan | 18 |
| pepe | 15 |
| marta | 15 |

- Verifiqué que el total cuadrara: 21+18+15+15 = 69, igual al total de filas antes de agrupar
- Observación: maria vendió casi el doble que pepe o marta — vale la pena investigar por qué en un análisis futuro

### Día 4 (Jueves) — Power Pivot: Modelo de datos y relaciones

**Parámetros (Power Query):**
- Un parámetro es una variable reutilizable: un valor central que varias fórmulas o reglas pueden usar
- Creé `UmbralAlta` (inicialmente 50,000) y lo conecté a mi columna condicional `Clasificacion`
- Verifiqué que funciona de verdad: al subir el parámetro a 60,000, una fila que antes decía "Alta" cambió a "Baja", sin tocar la fórmula — la actualización se propagó sola

**Power Pivot y relaciones:**
- El Modelo de datos permite conectar tablas sin copiar datos entre ellas (a diferencia de Merge, que sí copia los datos hacia la tabla principal)
- Creé una relación entre `ventas_febrero` y `productos`, usando "Producto" como columna en común

**Hallazgo clave — las relaciones filtran en una sola dirección:**

Intenté sumar `Precio` (de la tabla `productos`, el lado "uno") agrupado por `Region` (de la tabla `ventas_febrero`, el lado "muchos"), y el resultado fue el mismo total repetido en cada región (673,000 — la suma completa del catálogo). Esto NO era un error: las relaciones en el Modelo de datos filtran por defecto **solo desde la tabla "uno" hacia la tabla "muchos"**, nunca al revés.

La forma correcta es la inversa: agrupar `Monto` (de `ventas_febrero`, la tabla de hechos) por `Categoria` (de `productos`, la tabla de dimensión). Esa dirección sí funciona, porque un atributo de la tabla "uno" puede filtrar los datos de la tabla "muchos". Con esto obtuve:

| Categoría | Suma de Monto |
|---|---|
| Accesorios | ₡156,000 |
| Tecnología | ₡283,000 |
| (en blanco — Audífonos, sin match) | ₡273,000 |

Esta lógica de "tabla de hechos vs. tabla de dimensión" y dirección del filtro es la base conceptual de los modelos de Power BI que voy a ver en las Semanas 7-8.

**Choque de nombres — otro aprendizaje del día:**
Al intentar crear una relación usando la tabla `ventas` original (que ya había pasado por un Merge con `productos` el lunes), tenía dos columnas llamadas "Precio" — una copiada por el Merge, otra en la tabla `productos`. Usar Merge y relaciones sobre el mismo par de tablas genera ambigüedad; mejor elegir un solo enfoque por par de tablas.


### Mini-proyecto Semana 2 — ¿Qué categoría de producto genera más ingresos, y varía por vendedor?

**Metodología:** matriz cruzada (Categoría en filas, Vendedor en columnas, Suma de Monto en valores) usando la relación entre `ventas_febrero` y `productos` en el Modelo de datos.

| Categoría | juan | maria | marta | pepe | Total |
|---|---|---|---|---|---|
| Accesorios | — | 124,000 | 20,000 | 12,000 | 156,000 |
| Tecnología | 86,000 | 58,000 | 120,000 | 19,000 | 283,000 |

**Hallazgo de negocio:**
En Accesorios, María lidera claramente con ₡124,000 de los ₡156,000 totales (80% de la categoría). En Tecnología, en cambio, las ventas están más repartidas: Marta lidera con ₡120,000, seguida de Juan (₡86,000) y María (₡58,000). En conjunto, Tecnología generó más ingresos totales (₡283,000) que Accesorios (₡156,000).

**Alerta de calidad de datos:**
₡273,000 en ventas (repartidos entre Juan y María) corresponden al producto "Audífonos", que no está registrado en la tabla `productos` y por lo tanto no tiene Categoría asignada. Se debería investigar por qué falta este producto en el catálogo — probablemente debería clasificarse dentro de "Accesorios" — y corregirlo para tener un análisis completo y preciso.

## 📅 Semana 3: SQL Intensivo

**Estado: 🔄 En progreso**

### Día 1 (Lunes) — SQL básico: SELECT, WHERE, SUM, GROUP BY, primer JOIN

- Instalé DB Browser for SQLite como herramienta para escribir y ejecutar consultas
- Trabajé sobre una base de datos estilo Northwind (Productos, Categorias, Clientes, Pedidos, DetallesPedido — 5 tablas relacionadas)
- **Equivalencias que conecté con lo que ya sabía de Excel/Power Query:**

| Ya sabía (Excel/Power Query) | Ahora en SQL |
|---|---|
| SUMAR.SI / CONTAR.SI | `SUM()` / `COUNT()` + `WHERE` |
| Tabla dinámica / Agrupar por | `GROUP BY` |
| XLOOKUP / Merge | `JOIN` |
| Filtro de tabla | `WHERE` |

- `SELECT columna FROM tabla WHERE condición;` — sintaxis base
- `SELECT SUM(columna) FROM tabla WHERE condición;` — resume TODO en un solo número (no se puede mezclar con una columna de detalle sin agrupar, mismo problema conceptual que mezclar Filas/Valores mal en Power Pivot)
- `GROUP BY` — resuelve ese problema: una fila de resumen por categoría, no un solo total
- `JOIN ... ON tabla1.columna = tabla2.columna` — conecta dos tablas por una columna en común, igual que Merge. Por defecto es un **Inner Join**: solo trae lo que coincide en ambas tablas (equivalente a "Interna" en Power Query)
- Ejemplo: uní `Productos` con `Categorias` para reemplazar el `CategoriaID` (número) por el nombre real de la categoría

### Día 2 (Martes) — LEFT JOIN, JOIN de 3 tablas, ORDER BY

- `LEFT JOIN` — conserva todas las filas de la tabla principal aunque no haya match (equivalente a "Externa izquierda" en Power Query)
- **JOIN de 3 tablas (tabla "puente"):** `DetallesPedido` y `Clientes` no tienen ninguna columna en común entre sí — no se pueden conectar directo. Pero `Pedidos` sí comparte `PedidoID` con DetallesPedido, y `ClienteID` con Clientes, así que funciona como puente entre ambas:

```sql
SELECT Clientes.NombreCliente, Productos.NombreProducto, DetallesPedido.Cantidad
FROM DetallesPedido
JOIN Pedidos ON DetallesPedido.PedidoID = Pedidos.PedidoID
JOIN Clientes ON Pedidos.ClienteID = Clientes.ClienteID
JOIN Productos ON DetallesPedido.ProductoID = Productos.ProductoID;
```
- Resultado: 361 filas (el total de DetallesPedido), confirmando que cada detalle encontró su cliente y producto sin ningún hueco
- `ORDER BY columna DESC` — ordena resultados de mayor a menor (va al final de la consulta, después de cualquier WHERE/JOIN)
- **Concepto clave del día:** cuando dos tablas no comparten una columna directa, buscar una tercera tabla que sirva de puente entre ambas — mismo patrón que ya había visto con relaciones en Power Pivot la semana pasada