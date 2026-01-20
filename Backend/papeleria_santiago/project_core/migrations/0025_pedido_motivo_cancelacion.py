from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_core", "0024_pedido_remove_en_revision"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="motivo_cancelacion",
            field=models.TextField(blank=True, null=True),
        ),
    ]


