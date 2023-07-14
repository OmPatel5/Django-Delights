from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.IngredientList.as_view(), name="inventory"),
    path("menu-items/", views.menu_items, name="menu_items"),
    path("purchases/", views.purchases, name="purchases"),
    path("profit/", views.profit, name="profit"),
    
    
]