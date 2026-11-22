--Q1. Resumen mensual con las 4 palancas. Por anio_mes: pedidos, líneas, unidades, ingreso, ticket, líneas por pedido, unidades por línea y precio por unidad.--//
-- Q1
SELECT f.anio_mes AS mes,
       COUNT(DISTINCT v.pedido_id)                                AS pedidos,
       COUNT(*)                                                   AS lineas,
       SUM(v.cantidad)                                            AS unidades,
       ROUND(SUM(v.monto_linea), 2)                               AS ingreso,
       ROUND(SUM(v.monto_linea) / COUNT(DISTINCT v.pedido_id), 2) AS ticket,
       ROUND(1.0 * COUNT(*) / COUNT(DISTINCT v.pedido_id), 3)     AS lineas_x_pedido,
       ROUND(1.0 * SUM(v.cantidad) / COUNT(*), 3)                 AS unidades_x_linea,
       ROUND(SUM(v.monto_linea) / SUM(v.cantidad), 2)             AS precio_x_unidad
FROM fact_ventas_lineas v
JOIN dim_fecha f ON v.fecha_key = f.fecha_key
GROUP BY f.anio_mes
ORDER BY f.anio_mes;

--------------------
--Q2. Ranking, variación contra el mes anterior y acumulado (un CTE + RANK, LAG, SUM() OVER).
-- Q2
WITH mensual AS (
    SELECT f.anio_mes AS mes,
           COUNT(DISTINCT v.pedido_id) AS pedidos,
           ROUND(SUM(v.monto_linea), 2) AS ingreso
    FROM fact_ventas_lineas v
    JOIN dim_fecha f ON v.fecha_key = f.fecha_key
    GROUP BY f.anio_mes
)
SELECT mes, pedidos, ingreso,
       RANK() OVER (ORDER BY ingreso DESC) AS ranking_ingreso,
       ROUND(100.0 * (ingreso - LAG(ingreso) OVER (ORDER BY mes))
                   / LAG(ingreso) OVER (ORDER BY mes), 1) AS var_pct_vs_mes_anterior,
       ROUND(SUM(ingreso) OVER (ORDER BY mes), 2) AS ingreso_acumulado
FROM mensual
ORDER BY mes;

---------------------
-- Q3
WITH cm AS (
    SELECT f.anio_mes AS mes, p.nombre_categoria AS categoria,
           ROUND(SUM(v.monto_linea), 2) AS ingreso
    FROM fact_ventas_lineas v
    JOIN dim_fecha f    ON v.fecha_key = f.fecha_key
    JOIN dim_producto p ON v.producto_key = p.producto_key
    GROUP BY f.anio_mes, p.nombre_categoria
)
SELECT mes, categoria, ingreso
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY mes ORDER BY ingreso DESC) AS rn FROM cm)
WHERE rn = 1
ORDER BY mes;

---------------------
-- Q4
SELECT p.nombre_producto, p.precio_lista,
       SUM(v.cantidad) AS unidades,
       ROUND(SUM(v.monto_linea), 2) AS ingreso
FROM fact_ventas_lineas v
JOIN dim_fecha f    ON v.fecha_key = f.fecha_key
JOIN dim_producto p ON v.producto_key = p.producto_key
WHERE f.anio_mes = '2026-06'
GROUP BY p.nombre_producto, p.precio_lista
ORDER BY ingreso DESC
LIMIT 5;

----------------------
-- Q5
SELECT c.pais,
       COUNT(DISTINCT v.pedido_id) AS pedidos,
       ROUND(SUM(v.monto_linea), 2) AS ingreso,
       ROUND(100.0 * SUM(v.monto_linea) / SUM(SUM(v.monto_linea)) OVER (), 1) AS pct_del_total,
       ROUND(SUM(v.monto_linea) / COUNT(DISTINCT v.pedido_id), 2) AS ticket
FROM fact_ventas_lineas v
JOIN dim_cliente c ON v.cliente_key = c.cliente_key
GROUP BY c.pais
ORDER BY ingreso DESC;