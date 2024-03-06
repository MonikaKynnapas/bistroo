from datetime import datetime, date
from django import template

register = template.Library()


@register.filter
def is_menu_old(menu_date):
    date_object = datetime.strptime(menu_date, '%d.%m.%Y').date()
    today = date.today()  # Tänane kuupäev
    return date_object < today  # True või False