from django.db import models
import uuid
from pos_project.choices import EstadoEntidades  # Ajusta el import si tu proyecto cambia

class GrupoArticulo(models.Model):
    grupo_id = models.UUIDField(primary_key=True)
    nombre_grupo = models.CharField(max_length=50, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "grupos_articulos"
        ordering = ["nombre_grupo"]

class LineaArticulo(models.Model):
    linea_id = models.UUIDField(primary_key=True)
    codigo_linea = models.CharField(max_length=10, null=False)
    grupo = models.ForeignKey(
        GrupoArticulo,
        on_delete=models.RESTRICT,
        null=False,
        related_name='grupo_linea'
    )
    nombre_linea = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "lineas_articulos"
        ordering = ["codigo_linea"]

class CanalCliente(models.Model):
    canal_id = models.CharField(max_length=3, primary_key=True)
    nombre_canal = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "canal_cliente"
        ordering = ["nombre_canal"]

class Cliente(models.Model):
    cliente_id = models.UUIDField(primary_key=True)
    tipo_identificacion = models.CharField(max_length=1, null=False)
    no_identificacion = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=150, null=False)
    correo_electronico = models.EmailField(max_length=255, null=False)
    nro_mov = models.CharField(max_length=50, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    canal = models.ForeignKey(
        CanalCliente,
        on_delete=models.RESTRICT,
        null=False,
        related_name='clientes'
    )

    class Meta:
        db_table = "clientes"
        ordering = ["nombre"]

class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True)
    codigo_articulo = models.CharField(max_length=25, null=False)
    codigo_barras = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=150, null=False)
    presentacion = models.CharField(max_length=100, null=False)
    grupo = models.ForeignKey(
        GrupoArticulo,
        on_delete=models.RESTRICT,
        null=False,
        related_name='grupo_articulos'
    )
    linea = models.ForeignKey(
        LineaArticulo,
        on_delete=models.RESTRICT,
        null=False,
        related_name='linea_articulos'
    )
    stock = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    imagen = models.CharField(max_length=255, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "articulos"
        ordering = ["codigo_articulo"]

class ListaPrecio(models.Model):
    articulo = models.OneToOneField(
        Articulo,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='lista_precio'
    )
    precio_1 = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_2 = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_3 = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_4 = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2, null=False)

    class Meta:
        db_table = "lista_precios"
        ordering = ["articulo"]

class Pedido(models.Model):
    pedido_id = models.UUIDField(primary_key=True)
    no_pedido = models.CharField(max_length=20, null=False)
    fecha_pedido = models.DateTimeField(null=False)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        null=False,
        related_name='pedidos'
    )
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    importe = models.DecimalField(max_digits=12, decimal_places=2, null=False)

    class Meta:
        db_table = "pedidos"
        ordering = ["-fecha_pedido"]

class ItemPedido(models.Model):
    item_id = models.UUIDField(primary_key=True)
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        null=False,
        related_name='items_pedido'
    )
    nro_item = models.IntegerField(null=False)
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.RESTRICT,
        null=False,
        related_name='items_articulo'
    )
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    total_item = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "items_pedido"
        ordering = ["nro_item"]

