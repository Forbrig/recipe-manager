from django.shortcuts import render

from .models import Ingredients
# Create your views here.
def ingredient_detail_view(request):
    obj = Ingredients.objects.get()
    print(object)
    # context = {
    #     'title': obj.title,
    #     'description': obj.description,
    # }
    context = {
        'ingredients': obj,
    }
    return render(request, "ingredients/detail.html", context)