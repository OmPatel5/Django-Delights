from django.shortcuts import render
from django.views.generic import ListView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

# Create your views here.
def home(request):
    return render(request, "inventory/home.html")


class IngredientList(ListView):
    model = Ingredient
    template_name = 'inventory/ingredient_list.html'


def purchases(request):
    purchases = Purchase.objects.all()

    context = {'purchases': purchases}
    return render(request, 'inventory/purchases_list.html', context)

def get_ingredients():
    # get all menu items
    menu_items = MenuItem.objects.all()

    # get required ingredients for each item
    for item in range(len(menu_items)):
        menu_items[item].required_ingredients = RecipeRequirement.objects.filter(menu_item=menu_items[item])

    return menu_items



def menu_items(request):
    menu_items = get_ingredients()
         

    context = {'menu': menu_items}
    
    
    return render(request, 'inventory/menu_items_list.html', context)


def revenue(request):
    purchases = Purchase.objects.all()

    total_revenue = 0

    for purchase in purchases: 
        total_revenue += purchase.quantity * purchase.menu_item.price

    print(total_revenue)

    context = {'revenue': total_revenue}


    return render(request, 'inventory/revenue.html', context)


def cost(request):
    menu_items = get_ingredients()


    total_cost = 0

    # go thru all menu items
    for item in menu_items:
        # go thru all ingredients
        for ingredient in item.required_ingredients:
            # multiply price_per_unit by quantity_needed to get total_cost for that ingredient
            total_cost += ingredient.ingredient.price_per_unit * ingredient.quantity_needed

    context = {'cost': total_cost}

    return render(request, 'inventory/cost.html', context)
    
