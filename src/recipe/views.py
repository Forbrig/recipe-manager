import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from .models import Recipe, Ingredient, RecipeIngredient

def recipe_view(request):
    return render(request, 'recipe/recipe.html')

def recipe_list_all(request):
    if request.method == "POST":
        result = list(Recipe.objects.filter(deleted=False).values())

        html = ""
        for i in range(len(result)):
            ingrecipe = list(RecipeIngredient.objects.filter(recipe=result[i]['id']).values())
            totalRecipePrice = 0
            for j in range(len(ingrecipe)):
                ing = list(Ingredient.objects.filter(id=ingrecipe[j]['ingredient_id']).values())
                if len(ing) > 0:
                    totalIngredientPrice = ing[0]['price'] * ingrecipe[j]['ammount'] / ing[0]['ammount'] # price of the ingredient on the recipe
                    totalRecipePrice += totalIngredientPrice

            html +=  "<tr data='"+json.dumps(result[i], cls=DjangoJSONEncoder)+"'>"
            html +=     "<td>"+result[i]['name']+"</td>"
            html +=     "<td>"+result[i]['description']+"</td>"
            html +=     "<td>"+result[i]['preparation']+"</td>"
            html +=     "<td class='text-center'>"+str(totalRecipePrice)+"</td>"
            html +=     "<td class='text-center'>"
            html +=         "<i class='fa fa-pencil-alt sizeicon edit_recipe' title='Edit recipe.'></i>&nbsp&nbsp"
            html +=         "<i class='fa fa-trash-alt sizeicon delete_recipe text-danger' title='Delete recipe.'></i>"
            html +=     "</td>"
            html +=  "</tr>"

        context = {
            'code': 1,
            'msg': 'Recipes loaded.',
            'html': html,
        }
 
    return JsonResponse(context)

def recipe_save(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0: # if is an update
            # request.user
            Recipe.objects.filter(id=r['id']).update(name=r['name'], description=r['description'], preparation=r['preparation'])
            context = {
                'code': 1,
                'msg': 'Recipe updated.',
            }
        else: # if is a new insert
            query = Recipe(name=r['name'], description=r['description'], preparation=r['preparation'])
            query.save()
            context = {
                'code': 1,
                'msg': 'Recipe saved.',
            }

    return JsonResponse(context)

def recipe_delete(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0:
            Recipe.objects.filter(id=r['id']).update(deleted=True)
            context = {
                'code': 1,
                'msg': 'Recipe deleted.',
            }
        else:
            context = {
                'code': 2,
                'msg': 'Error.',
            }

    return JsonResponse(context)

def recipe_ingredient_save(request):
    if request.method == "POST":
        r = request.POST
      
        recipe = Recipe.objects.get(id=int(r['recipe']))
        ingredient = Ingredient.objects.get(id=int(r['ingredient']))

        result = list(RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient))

        if (len(result)) > 0: # update ingredient
            RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).update(ammount=r['ammount'], measureUnit=r['measureUnit'])
            context = {
                'code': 1,
                'msg': 'Ingredient of the recipe updated.',
            }
        else: # insert new ingredient
            query = RecipeIngredient(recipe=recipe, ingredient=ingredient, ammount=r['ammount'], measureUnit=r['measureUnit'])
            query.save()
            context = {
                'code': 1,
                'msg': 'Ingredient added in the recipe.',
            }

    return JsonResponse(context)

def recipe_ingredients_load(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0:

            # ingredient of the recipe (id of the ingredient and ammount)
            ingrecipe = list(RecipeIngredient.objects.filter(recipe=r['id']).values())
            # print(ingrecipe)
            totalRecipePrice = 0
            html = ""
            for i in range(len(ingrecipe)):
                ing = list(Ingredient.objects.filter(id=ingrecipe[i]['ingredient_id']).values())
                # print(ing)

                if len(ing) > 0:
                    totalIngredientPrice = ing[0]['price'] * ingrecipe[i]['ammount'] / ing[0]['ammount'] # price of the ingredient on the recipe
                    totalRecipePrice += totalIngredientPrice
                    ingrecipe[i]['price'] = str(totalIngredientPrice)
                    ingrecipe[i]['name'] = ing[0]['name']
                    ingrecipe[i]['measureUnit'] = ing[0]['measureUnit']

                    html +=  "<tr data='"+json.dumps(ingrecipe[i], cls=DjangoJSONEncoder)+"'>"
                    html +=     "<td>"+ing[0]['name']+"</td>"
                    html +=     "<td class='text-center'>"+str(ingrecipe[i]['ammount'])+ing[0]['measureUnit']+"</td>"
                    html +=     "<td class='text-center'>"+str(totalIngredientPrice)+"</td>"
                    html +=     "<td class='text-center'>"
                    html +=         "<i class='fa fa-pencil-alt sizeicon edit_recipe_ingredient' title='Edit recipe ingredient.'></i>&nbsp&nbsp"
                    html +=         "<i class='fa fa-trash-alt sizeicon delete_recipe_ingredient text-danger' title='Remove ingredient from recipe.'></i>"
                    html +=     "</td>"
                    html +=  "</tr>"

            context = {
                'code': 1,
                'msg': 'Ingredients of the recipe loaded.',
                'totalRecipePrice': totalRecipePrice,
                'html': html,
            }
        else:
            context = {
                'code': 2,
                'msg': 'Id of the recipe invalid.',
            }
 
    return JsonResponse(context)

def recipe_ingredient_delete(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0:
            RecipeIngredient.objects.filter(id=r['id']).delete()
            context = {
                'code': 1,
                'msg': 'Ingredient removed from recipe.',
            }
        else:
            context = {
                'code': 2,
                'msg': 'Error.',
            }
    return JsonResponse(context)

def autocomplete_ingredients(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        ingredients = Ingredient.objects.filter(deleted=False, name__icontains=query)
        results = []
        for ingredient in ingredients:
            place_json = {}
            place_json['id'] = ingredient.id
            place_json['label'] = ingredient.name
            place_json['name'] = ingredient.name
            place_json['price'] = str(ingredient.price)
            place_json['measure'] = ingredient.measureUnit
            place_json['ammount'] = ingredient.ammount
            
            results.append(place_json)
        result = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(result, mimetype)

def ingredient_view(request):
    return render(request, 'ingredient/ingredient.html')

def ingredient_list_all(request):
    if request.method == "POST":
        result = list(Ingredient.objects.filter(deleted=False).values())

        html = ""
        for i in range(len(result)):
            html +=  "<tr data='"+json.dumps(result[i], cls=DjangoJSONEncoder)+"'>"
            html +=     "<td>"+result[i]['name']+"</td>"
            html +=     "<td>"+result[i]['description']+"</td>"
            html +=     "<td class='text-center'>"+str(result[i]['ammount']) + result[i]['measureUnit']+"</td>"
            html +=     "<td class='text-center'>"+str(result[i]['price'])+"</td>"
            html +=     "<td class='text-center'>"
            html +=         "<i class='fa fa-pencil-alt sizeicon edit_ingredient' title='Edit ingredient.'></i>&nbsp&nbsp"
            html +=         "<i class='fa fa-trash-alt sizeicon delete_ingredient text-danger' title='Delete ingredient.'></i>"
            html +=     "</td>"
            html +=  "</tr>"

        context = {
            'code': 1,
            'msg': 'Ingredients loaded.',
            'html': html,
        }
 
    return JsonResponse(context)

def ingredient_save(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0: # if is an update
            # request.user
            Ingredient.objects.filter(id=r['id']).update(name=r['name'], description=r['description'], price=r['price'], measureUnit=r['measureUnit'], ammount=r['ammount'])
            context = {
                'code': 1,
                'msg': 'Ingredient updated.',
            }
        else: # if is a new insert
            query = Ingredient(name=r['name'], description=r['description'], price=r['price'], measureUnit=r['measureUnit'], ammount=r['ammount'])
            query.save()
            context = {
                'code': 1,
                'msg': 'Ingredient saved.',
            }

    return JsonResponse(context)

def ingredient_delete(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0:
            Ingredient.objects.filter(id=r['id']).update(deleted=True)
            context = {
                'code': 1,
                'msg': 'Ingredient deleted.',
            }
        else:
            context = {
                'code': 2,
                'msg': 'Error.',
            }

    return JsonResponse(context)

