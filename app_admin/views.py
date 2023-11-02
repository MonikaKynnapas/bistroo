import urllib.parse
from urllib.request import urlopen
import json

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from .forms import *
from .models import *

# Create your views here.


class HomeView(TemplateView):
    template_name = 'app_admin/index.html'


class CategoryCreateView(CreateView):
    template_name = 'app_admin/category_form_create.html'
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('app_admin:category_list')


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by('number')
    context_object_name = 'categories'


class CategoryUpdateView(UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    fields = ['number', 'name']
    success_url = reverse_lazy('app_admin:category_list')

    def form_valid(self, form):
        # Additional checks
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    template_name = 'app_admin/category_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')


class MenuCreateView(CreateView):
    template_name = 'app_admin/menu_form_create.html'
    model = Menu
    # fields = '__all__'
    form_class = MenuCreateForm
    success_url = reverse_lazy('app_admin:menu_list')

class MenuListView(ListView):
    template_name = 'app_admin/menu_list.html'
    model = Menu
    context_object_name = 'menus'


class MenuUpdateView(UpdateView):
    template_name = 'app_admin/menu_update.html'
    model = Menu
    fields = ['date', 'theme', 'recommends', 'prepared']
    success_url = reverse_lazy('app_admin:menu_list')

    def form_valid(self, form):
        # Additional checks
        return super().form_valid(form)


class MenuDeleteView(DeleteView):
    template_name = 'app_admin/menu_delete.html'
    model = Menu
    success_url = reverse_lazy('app_admin:menu_list')
