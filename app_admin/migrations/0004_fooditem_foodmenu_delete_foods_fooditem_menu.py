# Generated by Django 4.2.7 on 2023-11-22 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0003_foods'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.CharField(max_length=50)),
                ('full_price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('half_price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('show_in_menu', models.BooleanField(default=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['menu'],
            },
        ),
        migrations.CreateModel(
            name='FoodMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_admin.category')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_admin.menu')),
            ],
            options={
                'ordering': ['-date', 'category_id'],
            },
        ),
        migrations.DeleteModel(
            name='Foods',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_admin.foodmenu'),
        ),
    ]
