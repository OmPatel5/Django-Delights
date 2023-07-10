from django.shortcuts import render
from django.views.generic import ListView
from .models import Ingredient

# Create your views here.
def home(request):
    return render(request, "inventory/home.html")


class IngredientList(ListView):
    model = Ingredient
    template_name = 'inventory/inventory.html'