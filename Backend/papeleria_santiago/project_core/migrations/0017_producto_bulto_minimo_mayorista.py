from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0016_alter_comprobante_cedula_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='disponible_mayorista',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='bulto_minimo_mayorista',
            field=models.PositiveIntegerField(default=1),
        ),
    ]


