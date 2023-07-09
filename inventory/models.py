from django.db import models

# Create your models here.
class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=25)
    available_quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=10)
    price_per_unit = models.FloatField()

    def __str__(self):
        return f"{self.ingredient_name}: {self.price_per_unit}, {self.available_quantity}"

class MenuItem(models.Model):
    item_name = models.CharField(max_length=25)
    price = models.FloatField()

    def __str__(self):
        return f"{self.item_name}: {self.price}"

class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.menu_item.item_name
    
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField()

    def __str__(self):
        return f"Purchase: {self.menu_item}, Time: {self.purchase_time}"