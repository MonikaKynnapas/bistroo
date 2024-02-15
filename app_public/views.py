from urllib.request import urlopen
import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings
from .models import *
from datetime import datetime
from django.db.models import Q, Count
from app_admin.models import Menu, FoodMenu, FoodItem


# Create your views here.


class HomeView(TemplateView):
    template_name = 'app_public/index.html'
    model = Menu

    def get_context_data(self, **kwargs):
        all_data = None  # Sisaldab kogu menüü infot.
        today_string = datetime.today().strftime('%Y-%m-%d')  # 2024-01-24 #
        # today_string = '2023-11-24'  # Test, menu exists
        estonian_date = datetime.strptime(today_string, '%Y-%m-%d').strftime('%d.%m.%Y')

        try:
            today_menu_id = Menu.objects.get(date=today_string)  # Result one row or Error
            today_menu = Menu.objects.filter(Q(date=today_string)).values('date', 'theme', 'recommends', 'prepared')
            today_all_categories = FoodMenu.objects.filter(date_id=today_menu_id)

            all_data = (FoodItem.objects.filter(Q(menu_id__in=today_all_categories))
                        .values('menu_id', 'food', 'full_price', 'half_price', 'show_in_menu',
                                'menu__category__name', 'id', 'menu__category__number')
                        .annotate(decount=Count('menu_id')).order_by('menu__category__number', 'id'))

            # print(today_all_categories)
        except Menu.DoesNotExist:
            today_menu = None

        context = {
            'object_list': all_data,
            'menu': today_menu,
            'estonian_date': estonian_date,
        }

        return context


def custom500(request):
    from django.shortcuts import render
    return render(request, '500.html', status=500)


def custom404(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)