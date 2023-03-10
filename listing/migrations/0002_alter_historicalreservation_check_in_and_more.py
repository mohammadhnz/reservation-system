# Generated by Django 4.1.7 on 2023-02-28 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalreservation",
            name="check_in",
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalreservation",
            name="check_out",
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="check_in",
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="check_out",
            field=models.DateField(db_index=True),
        ),
    ]
