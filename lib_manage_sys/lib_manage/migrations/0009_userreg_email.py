# Generated by Django 4.2.14 on 2024-07-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lib_manage", "0008_usergetbooks_duedate"),
    ]

    operations = [
        migrations.AddField(
            model_name="userreg",
            name="email",
            field=models.EmailField(default=0, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]