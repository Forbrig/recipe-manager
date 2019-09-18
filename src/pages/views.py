from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def recipes_view(request, *args, **kwargs):
    return render(request, "recipes.html", {})

def ingredients_view(request, *args, **kwargs):
    return render(request, "ingredients.html", {})