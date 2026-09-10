SELECT NombreProducto, PrecioUnitario 
FROM Productos
WHERE PrecioUnitario > 
(SELECT AVG(precioUnitario) FROM Productos);


