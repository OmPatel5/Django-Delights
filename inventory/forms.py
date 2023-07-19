from django import forms 

from .models import Ingredient, RecipeRequirement, MenuItem, Purchase

class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeRequirementCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = '__all__'


class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'


class PurchaseForm(forms.ModelForm):
    class Meta: 
        model = Purchase
        fields = ['menu_item', 'quantity'] 


