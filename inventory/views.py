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
        menu_items[item].price = '${:,.2f}'.format(menu_items[item].price)

    return menu_items



def menu_items(request):
    menu_items = get_ingredients()
         

    context = {'menu': menu_items}
    
    
    return render(request, 'inventory/menu_items_list.html', context)


def revenue():
    purchases = Purchase.objects.all()

    total_revenue = 0

    for purchase in purchases: 
        total_revenue += purchase.quantity * purchase.menu_item.price

    return total_revenue

def cost():
    menu_items = get_ingredients()
    total_cost = 0

    # go thru all menu items
    for item in menu_items:
        # go thru all ingredients
        for ingredient in item.required_ingredients:
            # multiply price_per_unit by quantity_needed to get total_cost for that ingredient
            total_cost += ingredient.ingredient.price_per_unit * ingredient.quantity_needed

    print(total_cost)
    return total_cost

def profit(request):
    total_cost = cost()
    total_revenue = revenue()

    profit = total_revenue - total_cost

    context = {
        'cost': '${:,.2f}'.format(total_cost),
        'revenue': '${:,.2f}'.format(total_revenue),
        'profit': '${:,.2f}'.format(profit)
    }

    return render(request, "inventory/profit.html", context)


