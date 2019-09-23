"""recipe_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pages.views import home_view, recipes_view
from recipe.views import recipe_view, recipe_list_all, recipe_save, recipe_delete, autocomplete_ingredients, recipe_ingredient_save, recipe_ingredient_delete, recipe_ingredients_load, ingredient_view, ingredient_list_all, ingredient_save, ingredient_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('recipes/', recipe_view, name='recipes'),
    path('recipe_list', recipe_list_all),
    path('recipe_save', recipe_save),
    path('recipe_delete', recipe_delete),
    path('autocomplete_ingredients', autocomplete_ingredients),
    path('recipe_ingredients_load', recipe_ingredients_load),
    path('recipe_ingredient_save', recipe_ingredient_save),
    path('recipe_ingredient_delete', recipe_ingredient_delete),
    path('ingredients/', ingredient_view, name='ingredients'),
    path('ingredient_list', ingredient_list_all),
    path('ingredient_save', ingredient_save),
    path('ingredient_delete', ingredient_delete)
]