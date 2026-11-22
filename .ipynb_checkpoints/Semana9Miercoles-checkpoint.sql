-- 1
SELECT c.sales_channel, COUNT(*) AS ventas, ROUND(SUM(v.total_profit),2) AS ganancia
FROM fact_ventas v JOIN dim_canal c ON v.canal_key = c.canal_key
GROUP BY c.sales_channel;

-- 2
SELECT p.item_type, COUNT(*) AS ventas, ROUND(SUM(v.total_profit),2) AS ganancia
FROM fact_ventas v JOIN dim_producto p ON v.producto_key = p.producto_key
GROUP BY p.item_type ORDER BY ganancia DESC LIMIT 3;

-- 3
SELECT f.anio, ROUND(SUM(v.total_profit),2) AS ganancia
FROM fact_ventas v JOIN dim_fecha f ON v.fecha_pedido_key = f.fecha_key
GROUP BY f.anio ORDER BY f.anio;

-- 4
SELECT MIN(julianday(e.fecha) - julianday(p.fecha)) AS minimo,
       ROUND(AVG(julianday(e.fecha) - julianday(p.fecha)),2) AS promedio,
       MAX(julianday(e.fecha) - julianday(p.fecha)) AS maximo
FROM fact_ventas v
JOIN dim_fecha p ON v.fecha_pedido_key = p.fecha_key
JOIN dim_fecha e ON v.fecha_envio_key  = e.fecha_key;