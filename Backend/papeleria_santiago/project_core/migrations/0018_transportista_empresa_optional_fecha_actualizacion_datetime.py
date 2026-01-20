from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0017_producto_bulto_minimo_mayorista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportista',
            name='empresa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transportista',
            name='estado_entrega',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Preparando', 'Preparando'), ('Despachado', 'Despachado'), ('Entregado', 'Entregado')], default='Pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='transportista',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True, blank=True, null=True),
        ),
    ]


