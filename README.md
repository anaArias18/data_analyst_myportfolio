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

