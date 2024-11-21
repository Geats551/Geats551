# Generated by Django 5.1.2 on 2024-11-21 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="agriculturalproduct",
            name="click_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="agriculturalproduct",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.category",
            ),
        ),
    ]
