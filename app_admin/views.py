import urllib.parse
from urllib.request import urlopen
import json

from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, FormView)
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect

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


class FoodMenuListView(ListView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_list.html'


class FoodMenuUpdateView(SingleObjectMixin, FormView):
    model = FoodMenu
    form_class = FoodMenuUpdateForm
    template_name = 'app_admin/food_menu_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=FoodMenu.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=FoodMenu.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return FoodMenuFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('app_admin:food_menu_detail', kwargs={'pk': self.object.pk})


class FoodMenuDetailView(DetailView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_detail.html'


class FoodMenuDeleteView(DeleteView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_delete.html'
    success_url = reverse_lazy('app_admin:food_menu_list')


class FoodMenuCreateView(CreateView):
    model = FoodMenu
    form_class = FoodMenuCreateForm
    template_name = 'app_admin/food_menu_create.html'
    # fields = ['date', 'category', ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The author has been added'
        )

        return super().form_valid(form)
