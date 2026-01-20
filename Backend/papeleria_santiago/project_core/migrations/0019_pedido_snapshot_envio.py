from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0018_transportista_empresa_optional_fecha_actualizacion_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='ciudad_envio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='direccion_envio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='numero_casa_envio',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='codigo_postal_envio',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]


