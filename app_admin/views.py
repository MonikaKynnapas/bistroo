import urllib.parse
from datetime import datetime
from urllib.request import urlopen
import json

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, FormView)
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, Http404

from .forms import *
from .models import *


# Create your views here.

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class HomeView(ManagerRequiredMixin, TemplateView):
    template_name = 'app_admin/index.html'


class CategoryCreateView(ManagerRequiredMixin, CreateView):
    template_name = 'app_admin/category_form_create.html'
    model = Category
    form_class = CategoryForm
    #  fields = '__all__'
    success_url = reverse_lazy('app_admin:category_list')


class CategoryListView(ManagerRequiredMixin, ListView):
    model = Category
    form_class = CategoryForm
    queryset = Category.objects.order_by('number')
    context_object_name = 'categories'


class CategoryUpdateView(ManagerRequiredMixin, UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    form_class = CategoryForm
    #  fields = ['number', 'name']
    success_url = reverse_lazy('app_admin:category_list')

    def form_valid(self, form):
        # Additional checks
        return super().form_valid(form)


class CategoryDeleteView(ManagerRequiredMixin, DeleteView):
    template_name = 'app_admin/category_delete.html'
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('app_admin:category_list')


class MenuCreateView(ManagerRequiredMixin, CreateView):
    template_name = 'app_admin/menu_form_create.html'
    model = Menu
    # fields = '__all__'
    form_class = MenuCreateForm
    success_url = reverse_lazy('app_admin:menu_list')

    def post(self, request, *args, **kwargs):
        my_data = request.POST
        my_date = my_data['date']

        try:
            new_date =datetime.strptime(my_date, '%d.%m.%Y').strftime('%Y-%m-%d')
            my_data._mutable = True
            my_data['date'] = new_date
            my_data._mutable = False
        except ValueError:
            return super().post(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

class MenuListView(ManagerRequiredMixin, ListView):
    template_name = 'app_admin/menu_list.html'
    model = Menu
    context_object_name = 'menus'
    paginate_by = 10


class MenuUpdateView(ManagerRequiredMixin, UpdateView):
    template_name = 'app_admin/menu_update.html'
    model = Menu
    # fields = ['date', 'theme', 'recommends', 'prepared']
    success_url = reverse_lazy('app_admin:menu_list')
    form_class = MenuCreateForm
    def form_valid(self, form):
        # Additional checks
        return super().form_valid(form)


class MenuDeleteView(ManagerRequiredMixin, DeleteView):
    template_name = 'app_admin/menu_delete.html'
    model = Menu
    success_url = reverse_lazy('app_admin:menu_list')


class FoodMenuListView(ManagerRequiredMixin, ListView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_list.html'
    # ordering = ['date']
    paginate_by = 10


class FoodMenuUpdateView(ManagerRequiredMixin, SingleObjectMixin, FormView):
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


class FoodMenuDetailView(ManagerRequiredMixin, DetailView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_detail.html'


class FoodMenuDeleteView(ManagerRequiredMixin, DeleteView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_delete.html'
    success_url = reverse_lazy('app_admin:food_menu_list')


class FoodMenuCreateView(ManagerRequiredMixin, CreateView):
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


class ArchivePage(ManagerRequiredMixin, ListView):
    model = Menu
    template_name = 'app_admin/archive.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivePage, self).get_context_data(**kwargs)
        context['unique_dates'] = Menu.objects.all()
        return context


class SearchResultsPage(ManagerRequiredMixin, ListView):
    # https://stackoverflow.com/questions/62094267/redirect-if-query-has-no-result
    model = FoodItem
    template_name = 'app_admin/archive_search.html'
    allow_empty = False


    def get_queryset(self):
        query = self.request.GET.get('q')  # Info from form
        object_list = None
        if len(query) > 2:
            # https://labpys.com/how-to-implement-join-operations-in-django-orm/
            object_list = FoodItem.objects.select_related('menu').filter(food__icontains=query)

        return object_list

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(SearchResultsPage, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('app_admin:archive')


class OldMenuPage(ManagerRequiredMixin, ListView):
    model = Menu
    template_name = 'app_admin/archive_menu.html'

    def get_context_data(self, **kwargs):
        all_data = None
        query = self.request.GET.get('date')

        # https://stackoverflow.com/questions/71023649/listview-with-an-extra-argument
        if not query:
            query = self.kwargs['date']  # PP.KK.AAAA

        date_object = datetime.strptime(query, '%d.%m.%Y').date()
        today_string = date_object.strftime('%Y-%m-%d')
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
