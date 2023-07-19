from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientCreateForm, RecipeRequirementCreateForm, MenuItemCreateForm, PurchaseForm
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import logout

from django.core.exceptions import PermissionDenied



# Create your views here.
def home(request):
    return render(request, "inventory/home.html")

class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("home")
  template_name = "registration/signup.html"

def logout_request(request):
  logout(request)
  return redirect("home")


class IngredientList(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'inventory/ingredient_list.html'

@login_required
def purchases(request):
    purchases = Purchase.objects.all()

    for purchase in range(len(purchases)):
        purchases[purchase].menu_item.price = '${:,.2f}'.format(purchases[purchase].menu_item.price)

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


@login_required
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
        purchases = Purchase.objects.filter(menu_item=item).count()

        for ingredient in item.required_ingredients:
            # multiply price_per_unit by quantity_needed to get total_cost for that ingredient
            total_cost += ingredient.ingredient.price_per_unit * ingredient.quantity_needed * purchases

    print(total_cost)
    return total_cost

@login_required
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



class IngredientFormCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_create_form.html"
    form_class = IngredientCreateForm


class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete_form.html"
    success_url = "../../"


@login_required
def deleteIngredient(request, pk):
    ingredient = Ingredient.objects.get(id=pk)

    if request.method == 'POST':
        recipe_requirement = RecipeRequirement.objects.filter(ingredient=ingredient).first()
        if recipe_requirement != None:
            recipe_requirement.menu_item.is_available = False
            recipe_requirement.menu_item.save()
        ingredient.delete() 



        return redirect('ingredients')

    return render(request, 'inventory/ingredient_delete_form.html', {'object': ingredient})


class UpdateAvailability(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = "inventory/item_update_availability.html"
    fields = ['is_available']

class RecipeRequirementFormCreate(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/create_recipe_requirement_form.html"
    form_class = RecipeRequirementCreateForm

class MenuItemFormCreate(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory/menu_item_create_form.html"
    form_class = MenuItemCreateForm


@login_required
def purchaseMenuItem(request):
    form = PurchaseForm()

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            menu_item_id = request.POST.get('menu_item')
            menu_item = MenuItem.objects.get(id=menu_item_id) 
            required_ingredients = menu_item.reciperequirement_set.all()

            for required_ingredient in required_ingredients:

                if required_ingredient.ingredient.available_quantity - (int(request.POST.get('quantity')) * required_ingredient.quantity_needed) < 0:
                    raise Http404('Item(s) cannot be purchased. Not enough ingredients')
                else:
                    required_ingredient.ingredient.available_quantity -= int(request.POST.get('quantity')) * required_ingredient.quantity_needed

            
            for required_ingredient in required_ingredients:
                required_ingredient.ingredient.save()

            form.save()
            return redirect('../../purchases')



    context = {'form': form}
    return render(request, 'inventory/purchase_create_form.html', context)


class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_update_form.html"
    fields = '__all__'

    