# Generated by Django 4.2.7 on 2024-09-15 22:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taskselection", "0007_alter_task_sv"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
