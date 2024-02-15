from django.urls import path
from . import views

app_name = 'app_admin'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('menu_create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('menu_list/', views.MenuListView.as_view(), name='menu_list'),
    path('menu_update/<int:pk>/', views.MenuUpdateView.as_view(), name='menu_update'),
    path('menu_delete/<int:pk>/', views.MenuDeleteView.as_view(), name='menu_delete'),

    path('food_menu_list/', views.FoodMenuListView.as_view(), name='food_menu_list'),
    path('food_menu_create/', views.FoodMenuCreateView.as_view(), name='food_menu_create'),
    path('food_menu_update/<int:pk>/', views.FoodMenuUpdateView.as_view(), name='food_menu_update'),
    path('food_menu_detail/<int:pk>/', views.FoodMenuDetailView.as_view(), name='food_menu_detail'),
    path('food_menu_delete/<int:pk>/', views.FoodMenuDeleteView.as_view(), name='food_menu_delete'),

    path('archive/', views.ArchivePage.as_view(), name='archive'),
    path('archive_search/', views.SearchResultsPage.as_view(), name='archive-search'),
    path('archive_search/menu', views.OldMenuPage.as_view(), name='archive-search-menu'),
    path('archive_search/menu/date/<str:date>', views.OldMenuPage.as_view(), name='archive-search-menu-date'),
    ]
