from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.IngredientList.as_view(), name="inventory")
]