# Generated by Django 4.2.7 on 2024-01-24 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0005_alter_fooditem_menu_alter_menu_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='prepared',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='recommends',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='theme',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
