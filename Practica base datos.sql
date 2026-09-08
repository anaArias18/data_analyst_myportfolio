SELECT Clientes.NombreCliente, Productos.NombreProducto, DetallesPedido.Cantidad
FROM DetallesPedido
JOIN Pedidos ON DetallesPedido.PedidoID = Pedidos.PedidoID
JOIN Clientes ON Pedidos.ClienteID = Clientes.ClienteID
JOIN Productos ON DetallesPedido.ProductoID = Productos.ProductoID
ORDER BY Cantidad DESC;