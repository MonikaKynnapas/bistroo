from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Category(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name

    class Meta:
        """ Default result ordering """
        ordering = ['number']
        verbose_name_plural = 'categories'


class Menu(models.Model):
    date = models.DateField()
    theme = models.CharField(max_length=25, null=True, blank=True)
    recommends = models.CharField(max_length=25, null=True, blank=True)
    prepared = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return f'{self.date}, {self.theme}, {self.recommends}, {self.prepared}'

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'menu'

    def clean(self):
        if (self.theme is not None and self.recommends is None) or (self.recommends is not None and self.theme is None):
            raise ValidationError('Theme ja recommends peavad olema mõlemad täidetud')


class Foods(models.Model):
    date = models.DateField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255, null=True, blank=True)
    full_price = models.DecimalField(max_digits=4, decimal_places=2)
    half_price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    show_menu = models.BooleanField(default=True)

    def __str__(self):
        return (f'{self.date}, {self.category_id}, {self.food_name}, {self.full_price}, {self.half_price}, '
                f'{self.show_menu}')

    class Meta:
        ordering = ['-date', 'category_id']
