from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0020_pedido_pago_y_snapshot_contacto_alter_comprobante_metodo_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='costo_envio',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='comprobante',
            name='costo_envio',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True),
        ),
    ]


