from decimal import Decimal

from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.db.models import DecimalField, F, Value
from django.db.models.functions import Greatest, Least
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from .models import (
    Categoria,
    Cliente,
    Comprobante,
    DetalleCarrito,
    DetallePedido,
    FavoritosCliente,
    Inventario,
    Pedido,
    Precio,
    Producto,
    Subcategoria,
    Transportista,
    Carrito,
    Variante,
)

admin.site.site_header = "Papelería Santiago - Administración"
admin.site.site_title = "Papelería Santiago Admin"
admin.site.index_title = "Panel de administración"


# -----------------------------
# Helpers / filtros
# -----------------------------
class MarcaListFilter(admin.SimpleListFilter):
    title = "Marca"
    parameter_name = "marca_ci"

    def lookups(self, request, model_admin):
        # Evitar duplicados por mayúsculas/minúsculas
        values = (
            Producto.objects.exclude(marca__isnull=True)
            .exclude(marca__exact="")
            .values_list("marca", flat=True)
            .distinct()
        )
        seen = set()
        out = []
        for v in values:
            key = str(v).strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            out.append((key, v))
        return sorted(out, key=lambda x: str(x[0]))

    def queryset(self, request, queryset):
        val = (self.value() or "").strip().lower()
        if not val:
            return queryset
        return queryset.filter(marca__iexact=val)


class ClientesPendientesValidacionFilter(admin.SimpleListFilter):
    title = "Validación mayorista"
    parameter_name = "mayorista_validacion"

    def lookups(self, request, model_admin):
        return [
            ("pendientes", "Pendientes de validación (Empresa + PENDIENTE + link)"),
        ]

    def queryset(self, request, queryset):
        if self.value() != "pendientes":
            return queryset
        return queryset.filter(
            tipo_cliente=Cliente.EMPRESA,
            estado_cuenta=Cliente.PENDIENTE,
        ).exclude(url_validacion__isnull=True).exclude(url_validacion__exact="")


class PedidoTieneComprobanteFilter(admin.SimpleListFilter):
    title = "Tiene comprobante"
    parameter_name = "has_comprobante"

    def lookups(self, request, model_admin):
        return [
            ("si", "Sí"),
            ("no", "No"),
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val == "si":
            return queryset.exclude(comprobante_transferencia__isnull=True).exclude(comprobante_transferencia__exact="")
        if val == "no":
            return queryset.filter(comprobante_transferencia__isnull=True) | queryset.filter(comprobante_transferencia__exact="")
        return queryset


# -----------------------------
# Inlines (menos clicks)
# -----------------------------
class PrecioInline(admin.StackedInline):
    model = Precio
    extra = 0
    max_num = 1
    can_delete = False


class InventarioInline(admin.StackedInline):
    model = Inventario
    extra = 0
    max_num = 1
    can_delete = False


class TransportistaInline(admin.StackedInline):
    model = Transportista
    extra = 0
    max_num = 1
    can_delete = False
    fields = ("empresa", "numero_guia", "estado_entrega", "fecha_actualizacion")
    readonly_fields = ("fecha_actualizacion",)


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    autocomplete_fields = ("producto",)
    readonly_fields = ("precio_unitario", "subtotal_detalle_pedido", "iva_detalle_pedido", "descuento_detalle_pedido", "total_detalle_pedido")


# -----------------------------
# Acciones con confirmación (seguras)
# -----------------------------
class BulkDiscountForm(forms.Form):
    APPLY_TO_PUBLICO = "PUBLICO"
    APPLY_TO_MAYORISTA = "MAYORISTA"
    APPLY_TO_AMBOS = "AMBOS"
    APPLY_TO_CHOICES = [
        (APPLY_TO_PUBLICO, "Clientes naturales (público)"),
        (APPLY_TO_MAYORISTA, "Clientes mayoristas"),
        (APPLY_TO_AMBOS, "Ambos"),
    ]

    MODE_SET = "SET"
    MODE_ADD = "ADD"
    MODE_CHOICES = [
        (MODE_SET, "Establecer (reemplaza el descuento actual)"),
        (MODE_ADD, "Sumar (agrega al descuento actual)"),
    ]

    percent = forms.DecimalField(
        label="Porcentaje de descuento (%)",
        min_value=Decimal("0.00"),
        max_value=Decimal("95.00"),
        decimal_places=2,
        max_digits=5,
        help_text="Se guarda como porcentaje (0 a 95). Ej: 10 = 10%.",
    )
    apply_to = forms.ChoiceField(label="Aplicar a", choices=APPLY_TO_CHOICES)
    mode = forms.ChoiceField(
        label="Modo",
        choices=MODE_CHOICES,
        initial=MODE_SET,
        help_text="Para evitar doble descuento accidental, usa 'Establecer'.",
    )


class AddStockForm(forms.Form):
    cantidad = forms.IntegerField(
        label="Cantidad a sumar",
        min_value=1,
        help_text="Suma stock sin sobrescribir el valor actual.",
    )


class CancelPedidoForm(forms.Form):
    motivo = forms.CharField(
        label="Motivo de cancelación (se mostrará al usuario)",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )


# -----------------------------
# Admin "Herramientas" (custom views)
# -----------------------------
class ToolsBulkDiscountWizardForm(BulkDiscountForm):
    CRITERIO_SUBCATEGORIA = "SUBCATEGORIA"
    CRITERIO_VARIANTE = "VARIANTE"
    CRITERIO_MARCA = "MARCA"
    CRITERIO_CHOICES = [
        (CRITERIO_SUBCATEGORIA, "Subcategoría"),
        (CRITERIO_VARIANTE, "Variante"),
        (CRITERIO_MARCA, "Marca"),
    ]

    criterio = forms.ChoiceField(label="Criterio", choices=CRITERIO_CHOICES)
    subcategoria = forms.ModelChoiceField(
        label="Subcategoría",
        queryset=Subcategoria.objects.all().order_by("nombre_subcategoria"),
        required=False,
    )
    variante = forms.ModelChoiceField(
        label="Variante",
        queryset=Variante.objects.all().order_by("nombre_variante"),
        required=False,
    )
    marca = forms.CharField(
        label="Marca (ignora mayúsculas/minúsculas)",
        required=False,
        max_length=50,
        help_text="Ej: OfficePro / officepro.",
    )

    def clean(self):
        cleaned = super().clean()
        criterio = cleaned.get("criterio")
        subcategoria = cleaned.get("subcategoria")
        variante = cleaned.get("variante")
        marca = (cleaned.get("marca") or "").strip()

        if criterio == self.CRITERIO_SUBCATEGORIA and not subcategoria:
            self.add_error("subcategoria", "Selecciona una subcategoría.")
        if criterio == self.CRITERIO_VARIANTE and not variante:
            self.add_error("variante", "Selecciona una variante.")
        if criterio == self.CRITERIO_MARCA and not marca:
            self.add_error("marca", "Ingresa una marca.")

        cleaned["marca"] = marca
        return cleaned


def _tools_product_queryset_from_form(cleaned):
    criterio = cleaned["criterio"]
    if criterio == ToolsBulkDiscountWizardForm.CRITERIO_SUBCATEGORIA:
        return Producto.objects.filter(subcategoria=cleaned["subcategoria"])
    if criterio == ToolsBulkDiscountWizardForm.CRITERIO_VARIANTE:
        return Producto.objects.filter(variante=cleaned["variante"])
    # Marca (case-insensitive)
    return Producto.objects.filter(marca__iexact=(cleaned.get("marca") or "").strip())


def _tools_bulk_update_discounts(product_qs, percent: Decimal, apply_to: str, mode: str) -> int:
    """
    Actualiza Precio.* en bulk (eficiente y transaccional), con clamp 0..95.
    Retorna cantidad de filas afectadas.
    """
    percent = max(Decimal("0.00"), min(Decimal("95.00"), Decimal(percent)))
    df = DecimalField(max_digits=5, decimal_places=2)

    prices = Precio.objects.filter(producto__in=product_qs)

    updates = {}

    def clamp_expr(expr):
        return Least(Value(Decimal("95.00"), output_field=df), Greatest(Value(Decimal("0.00"), output_field=df), expr))

    if apply_to in (BulkDiscountForm.APPLY_TO_PUBLICO, BulkDiscountForm.APPLY_TO_AMBOS):
        if mode == BulkDiscountForm.MODE_SET:
            updates["descuento_publico"] = Value(percent, output_field=df)
        else:
            updates["descuento_publico"] = clamp_expr(F("descuento_publico") + Value(percent, output_field=df))

    if apply_to in (BulkDiscountForm.APPLY_TO_MAYORISTA, BulkDiscountForm.APPLY_TO_AMBOS):
        if mode == BulkDiscountForm.MODE_SET:
            updates["descuento_mayorista"] = Value(percent, output_field=df)
        else:
            updates["descuento_mayorista"] = clamp_expr(F("descuento_mayorista") + Value(percent, output_field=df))

    if not updates:
        return 0

    return prices.update(**updates)


def herramientas_index(request):
    # Dashboard simple: contadores + links rápidos (MVP)
    pedido_pending = Pedido.objects.filter(estado_pedido="Pendiente").count()
    pedido_cancel = Pedido.objects.filter(estado_pedido="Cancelado").count()
    transport_pending = Transportista.objects.filter(estado_entrega="Pendiente").count()
    clientes_mayoristas_pend = Cliente.objects.filter(
        tipo_cliente=Cliente.EMPRESA,
        estado_cuenta=Cliente.PENDIENTE,
    ).exclude(url_validacion__isnull=True).exclude(url_validacion__exact="").count()
    pedidos_transfer_pend_con_comp = (
        Pedido.objects.filter(estado_pedido="Pendiente", metodo_pago="Transferencia bancaria")
        .exclude(comprobante_transferencia__isnull=True)
        .exclude(comprobante_transferencia__exact="")
        .count()
    )

    ctx = {
        **admin.site.each_context(request),
        "title": "Herramientas",
        "counts": {
            "pedidos_pendientes": pedido_pending,
            "pedidos_cancelados": pedido_cancel,
            "transportistas_pendientes": transport_pending,
            "clientes_mayoristas_pendientes_validacion": clientes_mayoristas_pend,
            "pedidos_transferencia_pendientes_con_comprobante": pedidos_transfer_pend_con_comp,
        },
        "links": {
            "bulk_discounts": reverse("admin:ps_herramientas_descuentos"),
            "pedidos_pendientes": reverse("admin:project_core_pedido_changelist") + "?estado_pedido__exact=Pendiente",
            "pedidos_cancelados": reverse("admin:project_core_pedido_changelist") + "?estado_pedido__exact=Cancelado",
            "transportistas_pendientes": reverse("admin:project_core_transportista_changelist") + "?estado_entrega__exact=Pendiente",
            "clientes_mayoristas_pendientes_validacion": reverse("admin:project_core_cliente_changelist") + "?mayorista_validacion=pendientes",
            "pedidos_transferencia_pendientes_con_comprobante": (
                reverse("admin:project_core_pedido_changelist")
                + "?estado_pedido__exact=Pendiente&metodo_pago__exact=Transferencia+bancaria&has_comprobante=si"
            ),
        },
    }
    return TemplateResponse(request, "admin/project_core/tools_index.html", ctx)


def herramientas_descuentos(request):
    """
    Wizard (simple MVP):
    - eliges 1 criterio: subcategoría OR variante OR marca
    - defines descuento + target + modo
    - preview (N productos / N precios)
    - confirmación final y aplicar
    """
    preview = None

    if request.method == "POST":
        form = ToolsBulkDiscountWizardForm(request.POST)
        if form.is_valid():
            product_qs = _tools_product_queryset_from_form(form.cleaned_data)
            product_qs = product_qs.select_related("subcategoria", "variante").order_by("SKU")
            n_products = product_qs.count()
            n_prices = Precio.objects.filter(producto__in=product_qs).count()

            preview = {
                "n_products": n_products,
                "n_prices": n_prices,
                "sample": list(product_qs.values_list("SKU", "nombre")[:10]),
            }

            if "apply" in request.POST:
                with transaction.atomic():
                    updated = _tools_bulk_update_discounts(
                        product_qs,
                        percent=form.cleaned_data["percent"],
                        apply_to=form.cleaned_data["apply_to"],
                        mode=form.cleaned_data["mode"],
                    )
                messages.success(request, f"Listo. Precios actualizados={updated}.")
                return redirect(reverse("admin:ps_herramientas_descuentos"))
    else:
        form = ToolsBulkDiscountWizardForm(
            initial={
                "criterio": ToolsBulkDiscountWizardForm.CRITERIO_SUBCATEGORIA,
                "mode": BulkDiscountForm.MODE_SET,
                "apply_to": BulkDiscountForm.APPLY_TO_PUBLICO,
            }
        )

    ctx = {
        **admin.site.each_context(request),
        "title": "Herramientas · Descuentos masivos",
        "form": form,
        "preview": preview,
    }
    return TemplateResponse(request, "admin/project_core/tools_bulk_discounts.html", ctx)


def _patch_admin_site_urls():
    # Parche idempotente: agregar /admin/herramientas/ sin migrar a AdminSite custom.
    if getattr(admin.site, "_ps_tools_urls_patched", False):
        return

    original_get_urls = admin.site.get_urls

    def get_urls():
        urls = original_get_urls()
        custom = [
            path("herramientas/", admin.site.admin_view(herramientas_index), name="ps_herramientas"),
            path(
                "herramientas/descuentos/",
                admin.site.admin_view(herramientas_descuentos),
                name="ps_herramientas_descuentos",
            ),
        ]
        return custom + urls

    admin.site.get_urls = get_urls
    admin.site._ps_tools_urls_patched = True


_patch_admin_site_urls()

@admin.register(FavoritosCliente)
class FavoritosClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'producto', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'cliente', 'producto')
    search_fields = ('cliente__nombre', 'producto__nombre', 'producto__SKU')
    readonly_fields = ('fecha_creacion',)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cliente', 'fecha_creacion', 'fecha_actualizacion', 'estado_dinamico',
        'total_carrito_display' # Incluimos la propiedad calculada
    )
    # Requerido para que otros admins puedan usar autocomplete_fields apuntando a Carrito (admin.E040).
    search_fields = ("id", "cliente__nombre", "cliente__email")
    list_select_related = ("cliente",)

    def total_carrito_display(self, obj):
        # Accede a la propiedad @property total_carrito del modelo Carrito
        return f"${obj.total_carrito:,.2f}" # Formateado como moneda
    total_carrito_display.short_description = "Total del Carrito"


# -----------------------------
# Catálogos (autocomplete)
# -----------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nombre_categoria",)
    list_display = ("id", "nombre_categoria")


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nombre_subcategoria", "categoria__nombre_categoria")
    list_display = ("id", "nombre_subcategoria", "categoria")
    list_filter = ("categoria",)


@admin.register(Variante)
class VarianteAdmin(admin.ModelAdmin):
    search_fields = ("nombre_variante", "subcategoria__nombre_subcategoria")
    list_display = ("id", "nombre_variante", "subcategoria")
    list_filter = ("subcategoria",)


# -----------------------------
# Productos + Precios + Inventario
# -----------------------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "SKU",
        "nombre",
        "marca",
        "categoria",
        "subcategoria",
        "variante",
        "pvp_display",
        "pvm_display",
        "desc_publico_display",
        "desc_mayorista_display",
        "total_vendidos",
    )
    list_filter = ("categoria", "subcategoria", "variante", MarcaListFilter)
    search_fields = ("SKU", "nombre", "codigo_barras", "marca")
    ordering = ("SKU",)
    list_select_related = ("categoria", "subcategoria", "variante")
    autocomplete_fields = ("categoria", "subcategoria", "variante")
    inlines = (PrecioInline, InventarioInline)
    actions = ("action_apply_bulk_discount",)
    save_on_top = True

    @admin.display(description="PVP")
    def pvp_display(self, obj):
        try:
            return obj.precios.pvp
        except Exception:
            return None

    @admin.display(description="PVM")
    def pvm_display(self, obj):
        try:
            return obj.precios.pvm
        except Exception:
            return None

    @admin.display(description="Desc. público (%)")
    def desc_publico_display(self, obj):
        try:
            return obj.precios.descuento_publico
        except Exception:
            return None

    @admin.display(description="Desc. mayorista (%)")
    def desc_mayorista_display(self, obj):
        try:
            return obj.precios.descuento_mayorista
        except Exception:
            return None

    @admin.action(description="Aplicar descuentos masivos (público/mayorista)")
    def action_apply_bulk_discount(self, request, queryset):
        """
        Acción con confirmación:
        - Se usa el queryset actual (puedes filtrar por subcategoría/marca/variante).
        - Aplica al modelo Precio relacionado (descuento_publico / descuento_mayorista).
        - Evita errores: no permite negativos, clamp 0..95.
        """
        if "apply" in request.POST:
            form = BulkDiscountForm(request.POST)
            if form.is_valid():
                percent = form.cleaned_data["percent"]
                apply_to = form.cleaned_data["apply_to"]
                mode = form.cleaned_data["mode"]

                productos = list(queryset.values_list("SKU", flat=True))
                precios_qs = Precio.objects.select_related("producto").filter(producto__SKU__in=productos)

                updated = 0
                skipped = 0

                with transaction.atomic():
                    for precio in precios_qs:
                        changed = False
                        if apply_to in (BulkDiscountForm.APPLY_TO_PUBLICO, BulkDiscountForm.APPLY_TO_AMBOS):
                            if mode == BulkDiscountForm.MODE_SET:
                                new_val = percent
                            else:
                                new_val = (precio.descuento_publico or Decimal("0.00")) + percent
                            # clamp
                            new_val = max(Decimal("0.00"), min(Decimal("95.00"), new_val))
                            if precio.descuento_publico != new_val:
                                precio.descuento_publico = new_val
                                changed = True

                        if apply_to in (BulkDiscountForm.APPLY_TO_MAYORISTA, BulkDiscountForm.APPLY_TO_AMBOS):
                            if mode == BulkDiscountForm.MODE_SET:
                                new_val = percent
                            else:
                                new_val = (precio.descuento_mayorista or Decimal("0.00")) + percent
                            new_val = max(Decimal("0.00"), min(Decimal("95.00"), new_val))
                            if precio.descuento_mayorista != new_val:
                                precio.descuento_mayorista = new_val
                                changed = True

                        if changed:
                            precio.save(update_fields=["descuento_publico", "descuento_mayorista"])
                            updated += 1
                        else:
                            skipped += 1

                self.message_user(
                    request,
                    f"Listo. Precios actualizados={updated}, sin cambios={skipped}.",
                    level=messages.SUCCESS,
                )
                return redirect(request.get_full_path())
        else:
            form = BulkDiscountForm(initial={"mode": BulkDiscountForm.MODE_SET})

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirmar descuentos masivos",
            "queryset": queryset,
            "form": form,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "opts": self.model._meta,
            "action_name": "action_apply_bulk_discount",
        }
        return TemplateResponse(request, "admin/project_core/apply_bulk_discount.html", context)


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ("producto", "pvp", "pvm", "iva", "descuento_publico", "descuento_mayorista")
    list_select_related = ("producto",)
    search_fields = ("producto__SKU", "producto__nombre", "producto__marca")
    list_filter = ("producto__categoria", "producto__subcategoria", "producto__variante")


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "sku_display", "stock", "ubicacion_bodega")
    list_select_related = ("producto",)
    search_fields = ("producto__SKU", "producto__nombre", "producto__codigo_barras")
    list_filter = ("ubicacion_bodega", "producto__categoria", "producto__subcategoria")
    actions = ("action_add_stock",)
    save_on_top = True

    @admin.display(description="SKU")
    def sku_display(self, obj):
        try:
            return obj.producto.SKU
        except Exception:
            return None

    @admin.action(description="Sumar stock (sin sobrescribir)")
    def action_add_stock(self, request, queryset):
        if "apply" in request.POST:
            form = AddStockForm(request.POST)
            if form.is_valid():
                qty = int(form.cleaned_data["cantidad"])
                updated = queryset.update(stock=F("stock") + qty)
                self.message_user(request, f"Listo. Registros actualizados={updated}.", level=messages.SUCCESS)
                return redirect(request.get_full_path())
        else:
            form = AddStockForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirmar suma de stock",
            "queryset": queryset,
            "form": form,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "opts": self.model._meta,
            "action_name": "action_add_stock",
        }
        return TemplateResponse(request, "admin/project_core/add_stock.html", context)


# Personalizables: 
# Mostrar el coste total de pedidos en tiempo real:
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "fecha_pedido",
        "metodo_pago",
        "estado_pedido",
        "monto_total_display",
        "comprobante_link",
        "transportista_link",
    )
    list_filter = ("estado_pedido", "metodo_pago", PedidoTieneComprobanteFilter, "fecha_pedido")
    search_fields = ("id", "cliente__nombre", "cliente__email")
    date_hierarchy = "fecha_pedido"
    inlines = (DetallePedidoInline, TransportistaInline)
    actions = ("action_aprobar_transferencia", "action_cancelar_pedido")
    save_on_top = True

    readonly_fields = ("fecha_pedido", "monto_total_display", "comprobante_preview", "comprobante_link", "transportista_link")

    fieldsets = (
        ("Pedido", {"fields": ("cliente", "fecha_pedido", "estado_pedido", "metodo_pago", "costo_envio")}),
        ("Comprobante (transferencia)", {"fields": ("comprobante_link", "comprobante_preview", "motivo_cancelacion")}),
        ("Envío (snapshot)", {"fields": ("ciudad_envio", "direccion_envio", "numero_casa_envio", "codigo_postal_envio")}),
        ("Contacto (snapshot)", {"fields": ("cedula_envio", "telefono_envio", "referencia_envio")}),
    )

    def get_readonly_fields(self, request, obj=None):
        # Evitar cambios accidentales: preferir acciones desde listado para aprobar/cancelar.
        ro = list(super().get_readonly_fields(request, obj))
        ro.append("estado_pedido")
        return ro
   
    # Calcular el monto total basado en los detalle_pedidos existentes que pertenezcan a este pedido. 
    def monto_total_display(self, obj):
        return f"${obj.monto_total:,.2f}" # Formateado como moneda
    monto_total_display.short_description = "Monto Total" # Nombre de la columna en el admin

    @admin.display(description="Comprobante")
    def comprobante_link(self, obj):
        try:
            f = getattr(obj, "comprobante_transferencia", None)
            if not f:
                return "-"
            return format_html('<a href="{}" target="_blank" rel="noopener">Abrir comprobante</a>', f.url)
        except Exception:
            return "-"

    @admin.display(description="Vista previa")
    def comprobante_preview(self, obj):
        try:
            f = getattr(obj, "comprobante_transferencia", None)
            if not f:
                return "-"
            return format_html(
                '<img src="{}" style="max-width:420px; max-height:420px; border:1px solid #e5e7eb; border-radius:8px;" />',
                f.url,
            )
        except Exception:
            return "-"

    @admin.display(description="Transportista")
    def transportista_link(self, obj):
        try:
            t = getattr(obj, "transportista", None)
            if not t:
                return "-"
            url = reverse("admin:project_core_transportista_change", args=[t.id])
            return format_html('<a href="{}">Transportista #{}</a>', url, t.id)
        except Exception:
            return "-"

    @admin.action(description="Aprobar pedidos (transferencia)")
    def action_aprobar_transferencia(self, request, queryset):
        if "apply" in request.POST:
            # IMPORTANTE:
            # No usar queryset.update(...) aquí, porque eso NO dispara signals.
            # Para transferencias, dependemos de signals.py para crear Comprobante + Transportista
            # cuando el Pedido pasa de Pendiente -> Pagado.
            ids = list(queryset.values_list("id", flat=True))
            qs = Pedido.objects.select_related("cliente").filter(
                id__in=ids,
                metodo_pago="Transferencia bancaria",
                estado_pedido="Pendiente",
            )

            approved = 0
            with transaction.atomic():
                for pedido in qs:
                    pedido.estado_pedido = "Pagado"
                    pedido.motivo_cancelacion = None
                    pedido.save(update_fields=["estado_pedido", "motivo_cancelacion"])
                    approved += 1

            self.message_user(request, f"Listo. Pedidos aprobados={approved}.", level=messages.SUCCESS)
            return redirect(request.get_full_path())

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirmar aprobación de pedidos (transferencia)",
            "queryset": queryset,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "opts": self.model._meta,
            "action_name": "action_aprobar_transferencia",
            "form": None,
            "warning": "Solo se aprobarán pedidos Pendiente con método de pago Transferencia bancaria.",
        }
        return TemplateResponse(request, "admin/project_core/pedido_confirm.html", context)

    @admin.action(description="Cancelar pedidos (con motivo)")
    def action_cancelar_pedido(self, request, queryset):
        if "apply" in request.POST:
            form = CancelPedidoForm(request.POST)
            if form.is_valid():
                motivo = (form.cleaned_data.get("motivo") or "").strip() or None
                ids = list(queryset.values_list("id", flat=True))
                qs = Pedido.objects.filter(id__in=ids).exclude(estado_pedido="Pagado")
                updated = qs.update(estado_pedido="Cancelado", motivo_cancelacion=motivo)
                self.message_user(
                    request,
                    f"Listo. Pedidos cancelados={updated}. (No se cancelan pedidos ya Pagado.)",
                    level=messages.SUCCESS,
                )
                return redirect(request.get_full_path())
        else:
            form = CancelPedidoForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirmar cancelación de pedidos",
            "queryset": queryset,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "opts": self.model._meta,
            "action_name": "action_cancelar_pedido",
            "form": form,
            "warning": "Por seguridad, NO se cancelan pedidos con estado Pagado.",
        }
        return TemplateResponse(request, "admin/project_core/pedido_confirm.html", context)

@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'numero_factura', 'fecha_emision', 'estado_fiscal')
    search_fields = ('numero_factura', 'fecha_emision', 'estado_fiscal')
    list_filter = ('fecha_emision', 'estado_fiscal')


# -----------------------------
# Clientes mayoristas: validación rápida
# -----------------------------
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "tipo_cliente", "estado_cuenta", "email", "url_validacion_link")
    list_filter = ("tipo_cliente", "estado_cuenta", ClientesPendientesValidacionFilter)
    search_fields = ("nombre", "email", "cedula", "user__username")
    actions = ("action_validar_mayorista",)
    save_on_top = True
    readonly_fields = ("url_validacion_link",)

    fieldsets = (
        ("Cliente", {"fields": ("user", "nombre", "email", "telefono", "cedula", "ciudad", "direccion")}),
        ("Mayoristas", {"fields": ("tipo_cliente", "estado_cuenta", "url_validacion_link", "url_validacion")}),
    )

    @admin.display(description="URL validación")
    def url_validacion_link(self, obj):
        url = (getattr(obj, "url_validacion", None) or "").strip()
        if not url:
            return "-"
        return format_html('<a href="{}" target="_blank" rel="noopener">Abrir link</a>', url)

    @admin.action(description="Validar cliente mayorista (PENDIENTE → ACTIVO)")
    def action_validar_mayorista(self, request, queryset):
        # Solo Empresa + PENDIENTE + con url_validacion
        eligible = queryset.filter(
            tipo_cliente=Cliente.EMPRESA,
            estado_cuenta=Cliente.PENDIENTE,
        ).exclude(url_validacion__isnull=True).exclude(url_validacion__exact="")

        if "apply" in request.POST:
            # IMPORTANTE:
            # No usar update(...) porque:
            # - Cliente.save sincroniza User.is_active
            # - signals.py envía email cuando Empresa pasa a ACTIVO
            activated = 0
            with transaction.atomic():
                for cliente in eligible.select_related("user"):
                    cliente.estado_cuenta = Cliente.ACTIVO
                    cliente.save(update_fields=["estado_cuenta"])
                    activated += 1

            self.message_user(request, f"Listo. Clientes activados={activated}.", level=messages.SUCCESS)
            return redirect(request.get_full_path())

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirmar validación de clientes mayoristas",
            "queryset": eligible,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "opts": self.model._meta,
            "action_name": "action_validar_mayorista",
            "form": None,
            "warning": "Solo se activarán clientes Empresa en estado PENDIENTE con URL de validación.",
        }
        return TemplateResponse(request, "admin/project_core/cliente_confirm.html", context)


# -----------------------------
# Transportista: búsquedas y acceso directo
# -----------------------------
@admin.register(Transportista)
class TransportistaAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "pedido_id_display", "empresa", "numero_guia", "estado_entrega", "fecha_actualizacion")
    list_select_related = ("pedido",)
    search_fields = ("pedido__id", "empresa", "numero_guia")
    list_filter = ("estado_entrega", "empresa")
    save_on_top = True

    @admin.display(description="Pedido ID")
    def pedido_id_display(self, obj):
        try:
            return obj.pedido.id
        except Exception:
            return None


# -----------------------------
# Otros modelos (mantener registro simple)
# -----------------------------
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "producto", "cantidad", "precio_unitario", "total_detalle_pedido")
    search_fields = ("pedido__id", "producto__SKU", "producto__nombre")
    list_filter = ("pedido__estado_pedido",)
    autocomplete_fields = ("producto", "pedido")


@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    list_display = ("id", "carrito", "producto", "cantidad", "total_detalle_carrito")
    search_fields = ("carrito__id", "producto__SKU", "producto__nombre")
    autocomplete_fields = ("producto", "carrito")
