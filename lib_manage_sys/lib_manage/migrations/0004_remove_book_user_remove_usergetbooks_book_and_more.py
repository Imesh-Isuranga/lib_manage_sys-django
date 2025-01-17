# Generated by Django 4.2.14 on 2024-07-27 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lib_manage", "0003_book_user_usergetbooks"),
    ]

    operations = [
        migrations.RemoveField(model_name="book", name="user",),
        migrations.RemoveField(model_name="usergetbooks", name="book",),
        migrations.RemoveField(model_name="usergetbooks", name="user",),
        migrations.AddField(
            model_name="usergetbooks",
            name="book_id",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="usergetbooks",
            name="user_id",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
