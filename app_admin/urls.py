from django.urls import path
from . import views

app_name = 'app_admin'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('menu_create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('menu_list/', views.MenuListView.as_view(), name='menu_list'),
    path('menu_update/<int:pk>', views.MenuUpdateView.as_view(), name='menu_update'),
    path('menu_delete/<int:pk>', views.MenuDeleteView.as_view(), name='menu_delete'),
    ]
