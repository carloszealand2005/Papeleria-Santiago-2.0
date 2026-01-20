from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0019_pedido_snapshot_envio'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='cedula_envio',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='telefono_envio',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='referencia_envio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='metodo_pago',
            field=models.CharField(blank=True, choices=[('Tarjeta', 'Tarjeta'), ('Transferencia bancaria', 'Transferencia bancaria')], default='Tarjeta', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comprobante',
            name='metodo_pago',
            field=models.CharField(blank=True, choices=[('Tarjeta', 'Tarjeta'), ('Transferencia bancaria', 'Transferencia bancaria'), ('Tarjeta de crédito', 'Tarjeta de crédito'), ('Tarjeta de débito', 'Tarjeta de débito'), ('Cheque', 'Cheque')], max_length=50, null=True),
        ),
    ]


