# data_analyst_myportfolio

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

| Archivo | Descripción |
|---|---|
| `practica_semana1_dia1.xlsx` | Tabla base con referencias absolutas |
| *(archivo día 2-3)* | Fórmulas condicionales + XLOOKUP/BUSCARV |
| *(archivo día 4-5)* | Tablas dinámicas + Power Query |

---

## 🎯 Próximos pasos

- Semana 1 (cierre): mini-proyecto integrador (sábado) + repaso (domingo)
- Semana 2: Power Query avanzado
- Semanas 3-4: SQL intensivo

