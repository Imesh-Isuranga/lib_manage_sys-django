# Generated by Django 4.2.14 on 2024-07-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lib_manage", "0010_alter_userreg_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="usergetbooks",
            name="emailStatus",
            field=models.BooleanField(default=False),
        ),
    ]
