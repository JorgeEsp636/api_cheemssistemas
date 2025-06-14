# Generated by Django 5.2.1 on 2025-06-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0013_conductor_fecha_vencimiento_licencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductor',
            name='licencia_conduccion',
            field=models.IntegerField(db_column='licencia_conduccion', unique=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='placa',
            field=models.CharField(db_column='placa', max_length=20, unique=True),
        ),
    ]
