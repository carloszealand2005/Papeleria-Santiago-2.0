from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0009_cliente_ciudad'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreRegistroUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('password', models.CharField(max_length=128)),
                ('celular', models.CharField(blank=True, max_length=30, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True)),
                ('otp_code', models.CharField(max_length=6)),
                ('intentos', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]


