from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse


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
    date = models.DateField(blank=False, null=False, unique=True)
    theme = models.CharField(max_length=250, null=True, blank=True)
    recommends = models.CharField(max_length=250, null=True, blank=True)
    prepared = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y")}'
        # return self.date

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'menu'


class FoodMenu(models.Model):
    date = models.ForeignKey(Menu, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ['date', 'category_id']

    def get_absolute_url(self):
        return reverse('app_admin:food_menu_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.date} {self.category}'


class FoodItem(models.Model):
    menu = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, related_name='food_fooditem')
    food = models.CharField(max_length=50)
    full_price = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    half_price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    show_in_menu = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['menu']

    def __str__(self):
        return f'{self.menu}'
