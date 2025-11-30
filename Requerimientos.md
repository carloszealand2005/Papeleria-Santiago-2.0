-------------------
## Requerimientos para el proyecto Papelería Santiago
-------------------

Objetivo del proyecto: Brindar a los compradores naturales o mayoristas de la papelería Santiago una manera ágil, segura y fácil de hacer pedidos desde el portal web usando su tarjeta de débito o crédito, generando facturas a su nombre.


### 1: Requerimientos no funcionales.
* El sistema debe ser construido en Vue para frontend y Django para backend
* El sistema debe tener alto rendimiento y tiempos de respuesta muy cortos
* El sistema debe tener seguridad en el uso de los métodos de pago
* El sistema debe actualizar la información en la base de datos cuándo un usuario haga cualquier petición POST válida (comprar productos)

* Debe exponer una API en el frontend hacia la base de datos para realizar lo siguiente:
 * POST: Crear un nuevo registro Pedido en base a un usuario
 * POST: Crear un nuevo registro Cliente natural con los datos proporcionados en el frontend
 * POST: Crear un nuevo registro Cliente mayorista con los datos proporcionados en el frontend
 * POST: El sistema debe crear un registro de Comprobante una vez que una compra se haya pagado y procesado. 

 * PUT: Añadir un nuevo producto a un Pedido existente en base a un usuario
 * PUT: Actualizar stock reservado de un producto luego que se haya añadido a un carrito de compras o el tiempo de reserva haya expirado
 * PUT: Actualizar stock de un producto luego de que una compra se haya procesado   
 * PUT: Actualizar el estado de pedido a Pagado luego de que una compra se haya procesado

 * GET: Conseguir todos los productos que sean de X categoría
 * GET: Conseguir todos los productos que contengan X caracteres
 * GEt: Conseguir todos los productos que se encuentren entre X y Y rango de precio
 * GET: Conseguir todos los productos que sean de X categoría y que contengan X caracteres
 * GET: Conseguir todos los productos que sean de X categoría y que se encuentren entre X y Y rango de precio
 * GET: Conseguir todos los productos que sean de X categoría, se encuentren entre X y Y rango de precio y que contengan X caracteres
 * GET: Conseguir todos los productos que contengan X caracteres y se encuentren entre X y Y rango de precio. 




### 2: Requerimientos funcionales: 

* El sistema debe contar con una interfaz de usuario moderna y una experiencia de usuario fluida. Los botones como carrito de compras, registrarse o cuenta deben estar visibles en todas las partes de la aplicación. 


* El sistema debe permitir al usuario ver al usuario los productos disponibles en la base de datos. Organizándolos por: Categorías, búsquedas que coinciden, rangos de precios, marca. Si el usuario no está registrado en el sistema mostrará los precios por defecto para un cliente natural.

* El sistema debe permitir al usuario registrar productos como favoritos y poder acceder a ellos en cualquier parte de la interfaz. Si el usuario no está registrado e intenta añadir un producto favorito, enviar a la pantalla de registro. 

* El sistema debe permitir al usuario natural registrarse (Usando OAuth con Google o simplemente un correo con contraseña) con el aviso 'Registrate en menos de un minuto' al momento de añadir cualquier producto a su carrito vacío. Mientras el usuario no está registrado cualquier acción POST de crear un pedido será inválida.

* El sistema debe permitir al usuario mayorista ver la opción de 'Soy una empresa'. La interfaz requerirá input del usuario mayorista que tendrá que ser enviada. Un miembro de la administración revisará esta petición. El usuario mayorista ahora se le mostrarán los precios por unidad para todos los productos; así mismo como un bulto mínimo que se debe de comprar para obtener ese precio. Podrá añadir objetos al carrito y ver el total, pero si la cuenta no es confirmada el usuario no podrá proceder con el pago. 

* El sistema debe permitir al usuario natural añadir productos a su carrito de compras, creando un nuevo 'Pedido' cuándo se agrega cualquier producto a un carrito vacío y marcándolo como pendiente.
 
* El sistema debe permitir al usuario pagar con su tarjeta los productos que están actualmente en su carrito. 

* Tantos los clientes naturales y mayoristas deben ser capaces de ver un historial de sus compras/facturas. Si el cliente intenta acceder a esta función y no está registrado, mostrar aviso de registro. 




### 3: Flujo de compra: 
El sistema debe cumplir las siguientes reglas al momento de hacer una compra:
Un usuario al momento de añadir X productos a su carrito debe alterar la base de datos para que la cantidad de stock cambie su estado a reservado. Es decir,

```
(PSEUDOCÓDIGO)
Producto:
  stock_total = 100
  stock_reservado = 5   ← suma de los carritos activos

stock_disponible = stock_total - stock_reservado
```

Este stock_disponible es el que los demás usuarios recibirán al momento de visualizar todos los productos, incluidos en el carrito de compras.
Al pasar cierta cantidad de tiempo (1 hora), si el usuario no ha procedido con la compra se debe quitar de su cuenta el stock_reservado; el carrito de compras no perderá sus productos. 
Un proceso automático debe realizar:
```
(PSEUDOCÓDIGO)
si reserva.expira:
    stock_reservado -= cantidad
    eliminar ítem del carrito o marcar como caducado
```

Posterior a que haya expirado el producto, se debe mostrar un mensaje: 
⏳ La reserva de este producto ha expirado. 


### 4: Componentes para generar el diagrama de arquitectura del proyecto: 
 * Sistema de pagos
 * Sistema de autenticación de usuario (OAuth)
 * API Rest con peticiones: GET, POST, PUT
 * 


