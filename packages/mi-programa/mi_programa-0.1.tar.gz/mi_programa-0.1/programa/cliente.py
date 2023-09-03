class Cliente:
    def __initt__(self, nombre, email, direccion, telefono):
        self.nombre = nombre
        self.email = email
        self.direccion = direccion
        self.telefono = telefono
        self.carrito_compras = []

    def agregar_productos (self, producto, cantidad):
        self.carrito_compras.append({"Producto" : producto, "Cantidad" : cantidad })
        print(f"{cantidad} {producto.nombre}(s) agregado(s) al carrito de {self.nombre}")

    def eliminar_producto(self, producto, cantidad):
        for item in self.carrito_compras:
            if item ["Prodcuto"] == producto:
                if item["cantidad"] <= cantidad:
                    self.carrito_compras.remove(item)
                    print(f"{item['cantidad']} {producto.nombre}(s) eliminado(s) del carrito de {self.nombre}")
                else:
                    item["cantidad"] -= cantidad
                    print(f"{cantidad}{producto.nombre}(s) eliminado del carrito de {self.nombre}")
                return
            print(f" {producto.nombre} no está en el carrito de {self.nombre}")

    def ver_carrito(self):
        print(f"Carrito de {self.nombre}:")
        total = 0 
        for item in self.carrito_compras:
            producto = item["producto"]
            cantidad = item["cantidad"]
            subtotal = producto.precio * cantidad
            total += subtotal
            print (f"- {cantidad} {producto.nombre}: ${subtotal}")
        print(f"Total: ${total}")

    def __str__(self):
        return self.nombre
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio    

cliente1 = Cliente("Javier Milei", "lalivertadavanza@example.com", "altura 845 Calle Vera", "774-356-867")
producto1 = Producto("Camisa", 12800)
producto2 = Producto("Pantalon", 7000)

cliente1.agregar_producto(producto1, 2)
cliente1.agregar_producto(producto2, 3)
print(f"Cliente: {cliente1}")
cliente1.ver_carrito()

cliente1.eliminar_producto(producto2, 1)
cliente1.ver_carrito()
