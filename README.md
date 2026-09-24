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

### Día 3 (Miércoles) — Funciones de agregación avanzadas: COUNT, AVG, MAX, MIN, HAVING

**Funciones de agregación nuevas:**
- `COUNT()` — cuenta filas (equivalente a CONTAR.SI)
- `AVG()` — promedio
- `MAX()` / `MIN()` — valor más alto / más bajo
- Todas se combinan con `GROUP BY` cuando se necesita el resultado separado por categoría

**HAVING — filtrar después de agrupar:**
- `WHERE` filtra filas *antes* de agrupar (fila por fila)
- `HAVING` filtra el resultado *después* de agrupar (sobre los totales ya calculados)
- Ejemplo: encontrar clientes con más de 8 pedidos necesita `HAVING`, no `WHERE`, porque el conteo por cliente recién existe después del `GROUP BY`

```sql
SELECT ClienteID, COUNT(*) 
FROM Pedidos 
GROUP BY ClienteID 
HAVING COUNT(*) > 8;
```
→ Resultado: 4 de 20 clientes hicieron más de 8 pedidos

**Orden fijo de las cláusulas:**

**La regla de oro (el error que más se repitió hoy):**
Todo lo que va en el `SELECT` debe ser, o la columna por la que se agrupa (`GROUP BY`), o una función de agregación sobre una columna específica (`SUM()`, `AVG()`, `COUNT()`...). Nunca se puede dejar una columna de detalle suelta (como `NombreProducto` o `PedidoID`) junto a un resultado agrupado — SQL no sabría cuál de los múltiples valores posibles mostrar.

**Ejercicio guiado — combinar JOIN + GROUP BY + AVG:**

Armé paso a paso (primero el JOIN solo, después agregando la columna a resumir, y por último agrupando) una consulta que responde: ¿cuál es el precio promedio por categoría, usando el nombre real en vez del ID?

```sql
SELECT Categorias.NombreCategoria, AVG(Productos.PrecioUnitario) AS PromedioPorCategorias
FROM Productos
JOIN Categorias ON Productos.CategoriaID = Categorias.CategoriaID
GROUP BY Categorias.NombreCategoria;
```

- El `JOIN` trae el nombre real de la categoría (Productos solo tiene el ID)
- El `GROUP BY` resume 40 productos en 8 categorías
- Resultado: "Productos del Mar" tiene el precio promedio más alto de todas las categorías

**Aprendizaje del día:** cuando una consulta se pone difícil, conviene construirla en pasos — primero el JOIN solo (verlo funcionar), después agregar la columna a resumir sin tocar nada más, y recién al final envolver en la función de agregación y agrupar. Intentar escribir todo de una vez lleva a mezclar los mismos errores repetidos.

### Día 4 (Jueves) — Subconsultas (subqueries)

**¿Qué es una subconsulta?**
Una consulta SQL completa, escrita **dentro** de otra consulta (entre paréntesis), para responder preguntas que necesitan resolverse en dos pasos: primero un resultado intermedio, después usar ese resultado dentro de la consulta principal.

**Tipo 1 — Subconsulta con `NOT IN` (verificar pertenencia a una lista)**

Se usa cuando solo necesitás comprobar si algo *existe o no* en otra tabla, sin necesitar ningún otro dato combinado — por eso es más liviana que un `LEFT JOIN` para este caso específico.

```sql
SELECT NombreProducto
FROM Productos
WHERE ProductoID NOT IN (
    SELECT ProductoID FROM DetallesPedido
);
```
→ Pregunta: ¿qué productos nunca se vendieron?
→ Resultado: 0 filas — resultado válido, no un error. Significa que los 40 productos se vendieron al menos una vez.

**Tipo 2 — Subconsulta comparando contra un valor calculado**

Se usa cuando necesitás comparar cada fila contra un número que primero hay que calcular (como un promedio general), en vez de un número fijo escrito a mano.

```sql
SELECT NombreProducto, PrecioUnitario 
FROM Productos
WHERE PrecioUnitario > (
    SELECT AVG(PrecioUnitario) FROM Productos
);
```
→ La parte de adentro calcula un solo número (el promedio general)
→ La parte de afuera compara cada producto contra ese número, como si fuera un valor fijo
→ Resultado: 21 de 40 productos superan el precio promedio

**Cómo construir una subconsulta sin trabarse:**
1. Escribir primero la parte de **adentro sola**, y confirmar que funciona por sí misma
2. Después envolverla entre paréntesis, dentro del `WHERE` de la consulta principal
3. No intentar escribir las dos partes de una sola vez — separar el problema en pasos evita mezclar errores

**Recurso de refuerzo:** video de TodoCode sobre subconsultas SQL con práctica, para reforzar los dos tipos vistos hoy (WHERE con NOT IN y comparación con valor calculado).

### Día 5 (Viernes) — Funciones de fecha y CASE WHEN

**Funciones de fecha (SQLite):**
```sql
strftime('%m', FechaPedido)   → extrae el mes
strftime('%Y', FechaPedido)   → extrae el año
```
Se combinan con `GROUP BY` como cualquier otra columna — permite agrupar por mes, año, etc.

```sql
SELECT strftime('%m', FechaPedido) AS Mes, COUNT(*) AS CantidadPedidos
FROM Pedidos
GROUP BY strftime('%m', FechaPedido);
```
→ Resultado: 8 meses distintos con datos, Marzo lidera con 21 pedidos.

**CASE WHEN — el "SI" de SQL, con múltiples condiciones:**
```sql
SELECT DetalleID, Cantidad,
    CASE 
        WHEN Cantidad > 10 THEN 'Grande'
        ELSE 'Chico'
    END AS Clasificacion
FROM DetallesPedido;
```
→ Con 2 categorías posibles, alcanza con 1 `WHEN` explícito — el `ELSE` cubre el resto automáticamente. Resultado: distribución bastante pareja entre "Grande" y "Chico".

---

### Mini-proyecto Semana 3 — ¿Qué clientes gastaron más, y en qué categorías?

**Metodología:** consulta combinando 5 tablas (Clientes → Pedidos → DetallesPedido → Productos → Categorias), calculando el gasto real (Cantidad × PrecioUnitario) y agrupando por cliente y categoría.

**Construcción paso a paso** (la consulta más compleja de la semana, armada agregando un JOIN a la vez y verificando el conteo de filas en cada paso):

```sql
SELECT Clientes.NombreCliente, Categorias.NombreCategoria, 
       SUM(DetallesPedido.Cantidad * Productos.PrecioUnitario) AS GastoTotal
FROM Pedidos
JOIN Clientes ON Pedidos.ClienteID = Clientes.ClienteID
JOIN DetallesPedido ON Pedidos.PedidoID = DetallesPedido.PedidoID
JOIN Productos ON DetallesPedido.ProductoID = Productos.ProductoID
JOIN Categorias ON Productos.CategoriaID = Categorias.CategoriaID
GROUP BY Clientes.NombreCliente, Categorias.NombreCategoria
ORDER BY GastoTotal DESC;
```

**Hallazgos:**

El cliente con mayor gasto en una sola categoría es Mercado Andino, en Lácteos, con ₡2,071,637.18. El cliente más diversificado dentro del top 10 es Comercializadora Sol, que aparece fuerte en 3 categorías distintas — a diferencia de la mayoría, que se concentra en una o dos. En conjunto, el top 10 de gasto por categoría está dominado por solo 3 clientes (Mercado Andino, Comercializadora Sol y Tienda La Esquina), que ocupan la mayoría de los primeros puestos entre 2 o 3 categorías cada uno.

**Aprendizaje técnico del día:** una consulta con 4-5 JOINs se construye mucho mejor agregando una tabla a la vez y verificando el conteo de filas en cada paso, que intentando escribir todo de una sola vez.

---

## ✅ Repaso final — Semana 3 completa

**1. JOIN:** une tablas a partir de una columna en común. Sin especificar tipo, es un Inner Join — equivale a "Interna" en Power Query (solo lo que coincide en ambas tablas).

**2. LEFT JOIN:** conserva todos los registros de la tabla de la izquierda, y solo los coincidentes de la tabla de la derecha (equivale a "Externa izquierda" en Power Query).

**3. Tabla puente:** cuando dos tablas no comparten ninguna columna directamente, pero ambas comparten columnas distintas con una tercera tabla, esa tercera tabla sirve de "puente" para conectarlas con dos JOINs encadenados (ej: DetallesPedido y Clientes se conectan a través de Pedidos).

**4. WHERE vs. HAVING:** WHERE filtra filas individuales, antes de cualquier agrupamiento (sobre datos crudos). HAVING filtra el resultado ya resumido, después de que GROUP BY calculó los totales por grupo — por eso HAVING necesita que exista un GROUP BY primero.

**5. Dos tipos de subconsulta:**
- `NOT IN` → verificar si algo existe o no dentro de una lista generada por otra consulta
- Comparación con valor calculado → comparar cada fila contra un número que primero hay que calcular (ej. un promedio), en vez de un número fijo

**6. Regla de oro del SELECT:** todo lo que va en el SELECT debe ser, o la columna exacta del GROUP BY, o una función de agregación sobre otra columna. Nunca una columna de detalle suelta sin agrupar — SQL no sabría cuál valor mostrar entre los múltiples posibles.

**Semana 3 completa:** SQL básico (SELECT, WHERE, SUM, GROUP BY), JOINs (simple, LEFT, 3+ tablas encadenadas), funciones de agregación avanzadas (COUNT, AVG, MAX, HAVING), subconsultas, funciones de fecha, y CASE WHEN — todo aplicado sobre una base de datos relacional real (Northwind), no solo ejercicios aislados.

## Semana 4: SQL Avanzado

### Días 1-3 (Lunes-Martes-Miércoles) — Window Functions, CTEs, UNION y Self-Join

**Window Functions — resumir sin perder el detalle:**

`GROUP BY` colapsa varias filas en una sola por grupo — perdés el detalle individual. Las Window Functions resuelven esto: muestran cada fila completa, **y además** agregan un cálculo sobre su grupo, sin sacrificar nada.

```sql
SELECT 
    NombreProducto, 
    CategoriaID, 
    PrecioUnitario,
    ROW_NUMBER() OVER (PARTITION BY CategoriaID ORDER BY PrecioUnitario DESC) AS Ranking
FROM Productos;
```
- `PARTITION BY CategoriaID` → reinicia la numeración en cada categoría (como un GROUP BY, pero sin colapsar filas)
- `ROW_NUMBER()` vs `RANK()`: con empates exactos, RANK() da el mismo número a ambos y salta el siguiente; ROW_NUMBER() los numera distinto igual. En mi dataset no hubo empates de precio, así que ambas funciones dieron el mismo resultado — confirmé esto probando ambas, no solo asumiéndolo.
- Resultado: 5 productos por categoría, ranking de 1 a 5 dentro de cada una.

**CTEs (Common Table Expressions) — nombrar una subconsulta reutilizable:**

Equivalente a definir una función una sola vez y "llamarla" después, en vez de repetir la lógica completa cada vez. Especialmente útil en consultas largas con varios JOINs, donde mejora mucho la legibilidad.

```sql
WITH GastoPorClienteCategoria AS (
    SELECT Clientes.NombreCliente, Categorias.NombreCategoria, 
           SUM(DetallesPedido.Cantidad * Productos.PrecioUnitario) AS GastoTotal
    FROM Pedidos
    JOIN Clientes ON Pedidos.ClienteID = Clientes.ClienteID
    JOIN DetallesPedido ON Pedidos.PedidoID = DetallesPedido.PedidoID
    JOIN Productos ON DetallesPedido.ProductoID = Productos.ProductoID
    JOIN Categorias ON Productos.CategoriaID = Categorias.CategoriaID
    GROUP BY Clientes.NombreCliente, Categorias.NombreCategoria
)
SELECT NombreCliente, NombreCategoria, GastoTotal
FROM GastoPorClienteCategoria;
```
- Reescribí mi consulta del mini-proyecto de la Semana 3 (5 tablas) usando esta estructura
- El resultado es idéntico al original — un CTE no cambia el resultado, solo la organización y legibilidad de la consulta
- Partes de la sintaxis: `WITH nombre AS (` para abrir, la consulta completa adentro, `)` para cerrar, y un `SELECT ... FROM nombre` final para usarlo

**UNION — el "Append" de SQL:**

```sql
SELECT PedidoID FROM Pedidos WHERE Pais = 'Costa Rica'
UNION
SELECT PedidoID FROM Pedidos WHERE Pais = 'Mexico';
```
- Apila los resultados de dos consultas, igual que Append en Power Query
- `UNION` elimina duplicados automáticamente; `UNION ALL` los conserva
- **Matiz importante:** con una columna de identificador único (como PedidoID), no puede haber duplicados entre las dos consultas — por lo tanto UNION y UNION ALL dan exactamente el mismo resultado en este caso. La diferencia entre ambos solo se nota cuando sí es posible que se repitan filas idénticas.
- Resultado: 31 pedidos entre Costa Rica y México combinados

**Self-Join — una tabla conectada consigo misma (concepto, sin práctica):**

Útil cuando una tabla tiene una relación consigo misma (ej: un empleado con un "jefe" que también es empleado de la misma tabla). Se resuelve con JOIN usando dos alias distintos de la misma tabla. Northwind no tiene una columna así, por lo que quedó como concepto a tener presente para el futuro, sin ejercicio práctico hoy.

**Resumen de los 3 días:** Window Functions (detalle + resumen simultáneo), CTEs (subconsultas reutilizables y legibles), UNION (apilar resultados de consultas), y el concepto de Self-Join — cerrando los temas más avanzados de SQL antes del mini-proyecto final de la Semana 4.

### Mini-proyecto Semana 4 — ¿Cuál es el producto más caro de cada categoría, y cómo se compara con el promedio de su categoría?

**Metodología:** 2 CTEs conectados con JOIN — uno con Window Function (`ROW_NUMBER() OVER PARTITION BY`) para rankear productos dentro de su categoría, otro con el promedio por categoría (`GROUP BY` + `AVG`).

```sql
WITH RankedProducts AS (
    SELECT NombreProducto, CategoriaID, PrecioUnitario, 
           ROW_NUMBER() OVER (PARTITION BY CategoriaID ORDER BY PrecioUnitario DESC) AS Ranking
    FROM Productos
),
PromedioCategoria AS (
    SELECT CategoriaID, AVG(PrecioUnitario) AS PromedioCategoria
    FROM Productos 
    GROUP BY CategoriaID
)
SELECT NombreProducto, RankedProducts.CategoriaID, PrecioUnitario, PromedioCategoria
FROM RankedProducts
JOIN PromedioCategoria ON RankedProducts.CategoriaID = PromedioCategoria.CategoriaID
WHERE Ranking = 1;
```

**Por qué se necesitan 2 CTEs en vez de una sola consulta:** no se puede filtrar `WHERE Ranking = 1` en la misma consulta donde se calcula `ROW_NUMBER()`, porque las Window Functions se calculan *después* de que WHERE ya filtró las filas — en el momento del WHERE, la columna Ranking todavía no existe. Por eso el ranking se calcula primero dentro de un CTE, y recién se filtra por él en la consulta final, por fuera.

**Error encontrado y corregido:** `ambiguous column name: CategoriaID` — al tener dos CTEs con una columna del mismo nombre, hay que especificar de cuál viene cada una (`RankedProducts.CategoriaID`), igual que se hace al conectar tablas normales con JOIN.

**Hallazgos:**

El análisis muestra el producto más caro de cada categoría, comparado con el precio promedio de esa misma categoría. Tres productos destacan por tener una diferencia muy alta respecto a su promedio: Aguacates (2x el promedio, la diferencia más grande de toda la tabla), Sal Marina (también 2x) y Agua Mineral (1.6x). En el otro extremo, Yogur Natural es el más "típico" de su categoría, con su precio máximo apenas 22% por encima del promedio — la diferencia más pequeña de todas.

Esto podría interpretarse como una señal de negocio: en las categorías donde el producto más caro está muy por encima del promedio, probablemente hay un producto premium aislado entre varios productos baratos. En categorías como Lácteos, en cambio, los precios tienden a ser más parejos entre todos los productos.

---

## ✅ Repaso final — Semana 4 completa

**1. GROUP BY vs. Window Function:** GROUP BY colapsa todas las filas en una por grupo. Window Function conserva todas las filas originales, agregando el resultado del cálculo como una columna nueva, sin perder el detalle.

**2. CTE:** una tabla virtual temporal que modulariza una consulta compleja en partes aisladas, antes de combinarlas — simplifica la lógica y mejora la legibilidad, especialmente útil con múltiples CTEs conectados entre sí.

**3. UNION:** combina los resultados de dos o más consultas SELECT, eliminando filas duplicadas (no columnas). UNION y UNION ALL dan el mismo resultado cuando no es posible que existan filas duplicadas entre ambas consultas (ej: con una columna de ID único).

**4. Ambiguous column name:** ocurre cuando dos tablas o CTEs combinados tienen una columna con el mismo nombre, y no se especifica de cuál viene. Se soluciona indicando explícitamente la tabla/CTE de origen (`NombreTabla.Columna`).

**5. Por qué se necesita un CTE para filtrar por Window Function:** SQL calcula las Window Functions después de que WHERE ya filtró las filas — en el momento del WHERE, la columna calculada (como Ranking) todavía no existe. Por eso se calcula primero dentro de un CTE, y se filtra después en una consulta separada.

---

**Semana 4 completa — cierre del bloque de SQL (Semanas 3-4):** desde SELECT básico hasta CTEs encadenados con Window Functions y JOINs entre CTEs. Próximo bloque: Python + Pandas (Semana 5).

## Semana 5: Python + Pandas

### Día 1 (Lunes) — Fundamentos de Python y primer DataFrame

**Python básico:**
```python
nombre = "María"        # texto (string)
edad = 25                # entero (int)
precio = 19.99           # decimal (float)
activo = True             # booleano
ventas = [100, 250, 80]   # lista
```
Mismos tipos de dato que ya conocía de Excel/SQL (texto, número, fecha, booleano) — distinta sintaxis, mismo concepto de fondo.

**DataFrame — una tabla de Excel dentro de Python:**
```python
import pandas as pd
df = pd.read_csv("1000 Sales Records.csv")
```

**Comandos de exploración básica:**
```python
df.head()    # primeras 5 filas — equivalente a SELECT * FROM tabla LIMIT 5
df.shape     # (filas, columnas) → (1000, 14)
df.columns   # lista los nombres de columna
df.dtypes    # tipo de dato de cada columna
```

**Sobre `int64`:** el número no indica el valor máximo permitido de forma directa para el usuario común, sino la cantidad de *bits* que la computadora usa para guardar ese número en memoria. Más bits = puede guardar números más grandes, pero ocupa más espacio. Pandas usa 64 bits por defecto como margen de seguridad, aunque para un dataset de 1000 filas la diferencia de memoria es insignificante — donde sí importa es en datasets de millones de filas.

---

**Configuración del entorno — problemas reales resueltos:**

Antes de llegar a cargar el primer DataFrame, tuve que resolver varios obstáculos de configuración, en orden:

1. **Entorno virtual (venv) no encontrado:** el que había creado en la Semana 0 no estaba en la carpeta actual — lo recreé directo dentro de "Data Analyst" con `python -m venv data-analyst-env`.

2. **Error de permisos al activar:** PowerShell bloqueaba `Activate.ps1` por política de seguridad. Se resuelve una sola vez por cuenta de Windows con:


3. **`.gitignore` para excluir el entorno virtual del repositorio** — creado con la línea `data-analyst-env/`, para no subir a GitHub los archivos internos de Python (pesados e innecesarios como código propio).

4. **`jupyter` no reconocido:** pasaba porque el entorno virtual no estaba activo en ese momento — jupyter vive *dentro* del entorno, no en el Python global de Windows. Solución: activar el entorno antes de correr `jupyter notebook`.

5. **Archivo `.py` en vez de `.ipynb`:** al crear el notebook por primera vez, elegí sin darme cuenta "Python File" en vez de "Notebook" — un `.py` no tiene celdas ejecutables con Shift+Enter como un notebook real.

6. **CSV guardado en la carpeta equivocada:** el archivo terminó dentro de `data-analyst-env` (la carpeta del entorno) en vez de `Data Analyst` (donde vive el resto del trabajo) — lo moví al lugar correcto con el Explorador de Windows.

7. **Notebook ejecutándose desde una subcarpeta distinta:** usando `os.getcwd()` descubrí que Jupyter estaba corriendo desde `Data Analyst\Semana 2`, no desde `Data Analyst` donde está el CSV — por eso `FileNotFoundError` a pesar de que el archivo "estaba ahí cerca".

8. **Mover el notebook con Jupyter abierto rompió su referencia interna de ruta**, generando un error de guardado con una ruta duplicada/corrupta. Solución real: cerrar Jupyter completamente (Ctrl+C en la terminal), y volver a abrirlo desde cero, parada en la carpeta correcta, creando el notebook nuevo ahí directamente — sin moverlo después.

**Aprendizaje general del día:** los problemas de configuración de entorno (rutas, permisos, carpetas) son tan parte del trabajo real de un analista como la sintaxis de Pandas en sí. Diagnosticar con herramientas simples (`os.getcwd()`, revisar el Explorador de Windows) antes de asumir que algo está "roto" ahorra mucho tiempo.

### Día 2 (Martes) — Selección y filtrado de datos con Pandas

**Seleccionar columnas:**
```python
df["Region"]                                    # una columna (corchete simple)
df[["Region", "Total Profit"]]                   # varias columnas (doble corchete)
```

**Filtrar filas — el WHERE de Pandas:**

A diferencia de SQL, donde `WHERE` es una palabra clave, en Pandas el filtro se arma con una condición booleana dentro de corchetes:

```python
df[df["Total Profit"] > 100000]
```

- `df["Total Profit"] > 100000` por sí sola genera una lista de True/False, una por fila (confirmé esto corriéndola sin el `df[...]` de afuera)
- Envolver eso en `df[...]` hace que Pandas devuelva solo las filas marcadas como True
- Resultado: 747 de 1000 filas tienen ganancia mayor a 100,000

**Múltiples condiciones combinadas:**

En Pandas no se usa `and`/`or` de Python normal — se usan los símbolos `&` (Y) y `|` (O), y cada condición individual necesita sus propios paréntesis:

```python
df[(df["Total Profit"] > 100000) & (df["Sales Channel"] == "Online")]
```
→ Resultado: 354 filas (menos que las 747 de una sola condición, porque ahora se exigen ambas condiciones a la vez)

**Combinar filtro + selección de columnas:**

```python
df[df["Region"] == "Europe"][["Region", "Item Type", "Total Profit"]]
```
→ Primero se filtran las filas (solo Europa), después se seleccionan las columnas deseadas de ese resultado ya filtrado. El orden importa: filtro primero, columnas después.
→ Resultado: 267 filas de Europa, con solo 3 columnas.

**Problema de sesión resuelto:** al reabrir el notebook en una sesión nueva, el kernel se reinicia y las variables (como `df`) dejan de existir en memoria, aunque el código siga visible en las celdas. Hay que volver a correr la celda de carga (`import pandas`, `read_csv`) antes de usar `df` en cualquier celda nueva. Tip para el futuro: usar "Run All Cells" al reabrir un notebook, en vez de correr celdas sueltas de arriba.

**Equivalencias con lo que ya sabía:**

| SQL / Excel | Pandas |
|---|---|
| `WHERE columna > valor` | `df[df["columna"] > valor]` |
| `WHERE cond1 AND cond2` | `df[(cond1) & (cond2)]` |
| `SELECT col1, col2` | `df[["col1", "col2"]]` |


### Día 3-4 (Miércoles-Jueves) — GroupBy y Merge de DataFrames en Pandas

**GroupBy — el GROUP BY de SQL / Agrupar por de Power Query, en Pandas:**

```python
df.groupby("Region")["Total Profit"].sum()    # suma por grupo
df.groupby("Region")["Total Profit"].mean()   # promedio por grupo
df.groupby("Region")["Total Profit"].count()  # conteo por grupo

# Las 3 métricas juntas de una sola vez:
df.groupby("Region")["Total Profit"].agg(["sum", "mean", "count"])
```

**Hallazgo de negocio:** Europa domina en ganancia total (₡106.7M) porque tiene casi el triple de ventas (267) que Central America and the Caribbean (99) — pero Central America tiene el promedio de ganancia por venta más alto (₡417,543), lo que la hace más "eficiente" por transacción aunque genere menos ingreso total. Mismo patrón que ya había visto en el mini-proyecto de la Semana 1 (North America con menor volumen pero mejor margen) — un caso más de que "quién gana más en total" y "quién es más eficiente" pueden ser respuestas distintas a preguntas distintas.

**Nota técnica:** los resultados de `.sum()` a veces aparecen en notación científica (ej. `1.067720e+08`), que equivale a 106,772,000 — no es un error, es solo la forma en que Python muestra números grandes por defecto.

---

**Merge de DataFrames — el JOIN de SQL / Merge de Power Query, en Pandas:**

```python
pd.merge(df1, df2, on="columna_en_comun", how="inner")
```

| Parámetro `how` | Equivalente |
|---|---|
| `"inner"` | Inner Join (SQL) / "Interna" (Power Query) |
| `"left"` | LEFT JOIN (SQL) / "Externa izquierda" (Power Query) |
| `"right"` | RIGHT JOIN (SQL) / "Externa derecha" (Power Query) |
| `"outer"` | Full Outer Join |

**Comprobación práctica con datos reales:** creé una tabla pequeña `Region → Continente` con solo 4 de las 7 regiones existentes en el dataset (a propósito, dejando 3 afuera), para comparar `how="left"` vs. `how="inner"`:

- `how="left"` → 1000 filas (todas conservadas). Las regiones sin match en la tabla pequeña (Middle East and North Africa, Central America and the Caribbean, Australia and Oceania) aparecieron con `NaN` en la columna Continente, sin desaparecer.
- `how="inner"` → 684 filas. Las filas sin match se eliminaron completamente (1000 - 684 = 316 filas correspondientes a esas 3 regiones).

**Confirmación:** mismo comportamiento que ya había visto con "Audífonos" en Power Query (Semana 2) y con LEFT JOIN en SQL (Semana 3) — tres herramientas distintas, mismo concepto de fondo.

**Error de sintaxis resuelto:** dos instrucciones de Python escritas en la misma línea sin salto de línea entre ellas causan `SyntaxError: invalid syntax`. Cada instrucción necesita su propia línea.

**Equivalencias consolidadas — 3 herramientas, mismo concepto:**

| Concepto | SQL | Power Query | Pandas |
|---|---|---|---|
| Agrupar y resumir | `GROUP BY` | Agrupar por | `.groupby()` |
| Unir tablas (solo coincidencias) | `JOIN` / Inner Join | Externa/Interna | `how="inner"` |
| Unir conservando todo de un lado | `LEFT JOIN` | Externa izquierda | `how="left"` |