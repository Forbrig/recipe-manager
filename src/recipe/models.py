from django.db import models

MEASURE_UNIT_CHOICES = (
    ("g", "grams"),
    ("kg", "kilograms"),
    ("cl", "centiliter"),
    ("l", "liter")
)

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    preparation = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)

class Ingredient(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2) # 7 digits = 1 million €
    measureUnit = models.CharField(max_length=10, choices=MEASURE_UNIT_CHOICES)
    ammount = models.IntegerField()
    deleted = models.BooleanField(default=False)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) # when a recipe is deleted remove all ingredients ligation
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT) # do not let the ingredient to be deleted
    ammount = models.IntegerField()
    # this allows to track the measure units that have relation
    # ex: an ingredient saved with measure of 1 kg per 1€ will be displayed as 100g per 0.10€
    measureUnit = models.CharField(max_length=10, choices=MEASURE_UNIT_CHOICES) 
