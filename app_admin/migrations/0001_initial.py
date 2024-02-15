# Generated by Django 4.2.7 on 2023-11-01 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=225)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['number'],
            },
        ),
    ]