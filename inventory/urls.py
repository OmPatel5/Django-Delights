from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("logout/", views.logout_request, name="logout"),


    path("ingredients/", views.IngredientList.as_view(), name="ingredients"),
    path("menu-items/", views.menu_items, name="menu_items"),
    path("purchases/", views.purchases, name="purchases"),
    path("profit/", views.profit, name="profit"),

    path("ingredients/create/", views.IngredientFormCreate.as_view(), name="create_ingredient"),
    path("ingredients/<str:pk>/delete/", views.deleteIngredient, name="delete_ingredient"),

    path("menu-items/<str:pk>/update-availability", views.UpdateAvailability.as_view(), name="update_menu_item_availability"),

    path("recipe-requirement/create/", views.RecipeRequirementFormCreate.as_view(), name="create_recipe_requirement"),
    path("menu-items/create/", views.MenuItemFormCreate.as_view(), name="create_menu_item"),

    path('purchases/create/', views.purchaseMenuItem, name="purchase_menu_item"),

    path('ingredients/<str:pk>/update', views.IngredientUpdate.as_view(), name="update_ingredient")

    
    
]