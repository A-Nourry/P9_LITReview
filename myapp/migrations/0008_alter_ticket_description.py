# Generated by Django 4.1 on 2022-08-31 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0007_alter_review_comment_alter_ticket_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="description",
            field=models.CharField(max_length=6000, verbose_name="description"),
        ),
    ]
