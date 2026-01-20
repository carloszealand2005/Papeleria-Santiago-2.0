from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0021_pedido_costo_envio_and_comprobante_costo_envio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comprobante',
            name='url_factura',
        ),
        migrations.AddField(
            model_name='comprobante',
            name='comprobante_transferencia_archivo',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to='comprobantes_transferencia/'),
        ),
    ]


