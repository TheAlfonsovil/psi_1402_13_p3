# Generated by Django 2.1.7 on 2019-11-12 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0008_auto_20191112_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
