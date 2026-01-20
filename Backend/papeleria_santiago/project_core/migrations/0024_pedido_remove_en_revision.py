from django.db import migrations, models


def forwards_map_en_revision_to_pendiente(apps, schema_editor):
    Pedido = apps.get_model("project_core", "Pedido")
    # Migración de datos: eliminar el valor legacy "En revisión"
    Pedido.objects.filter(estado_pedido="En revisión").update(estado_pedido="Pendiente")


def backwards_map_pendiente_to_en_revision(apps, schema_editor):
    Pedido = apps.get_model("project_core", "Pedido")
    # Reversión conservadora: si vuelves atrás, no podemos saber cuáles Pendiente eran transferencias.
    # Por seguridad, NO convertimos Pendiente -> En revisión.
    return


class Migration(migrations.Migration):
    dependencies = [
        ("project_core", "0023_pedido_comprobante_transferencia_and_more"),
    ]

    operations = [
        migrations.RunPython(
            forwards_map_en_revision_to_pendiente,
            backwards_map_pendiente_to_en_revision,
        ),
        migrations.AlterField(
            model_name="pedido",
            name="estado_pedido",
            field=models.CharField(
                choices=[("Pendiente", "Pendiente"), ("Pagado", "Pagado"), ("Cancelado", "Cancelado")],
                max_length=20,
            ),
        ),
    ]


