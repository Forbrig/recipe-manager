import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.http import JsonResponse

from .models import Ingredients

def ingredients_view(request):
    return render(request, 'ingredients/detail.html')

# list of the ingredients
def ingredients_list_all(request):
    if request.method == "POST":
        result = list(Ingredients.objects.filter(deleted=False).values())

        html = ""
        for i in range(len(result)):
            html +=  "<tr data='"+json.dumps(result[i], cls=DjangoJSONEncoder)+"'>"
            html +=     "<td>"+result[i]['title']+"</td>"
            html +=     "<td>"+result[i]['description']+"</td>"
            html +=     "<td class='text-center'>"+result[i]['ammount'] + result[i]['measureUnit']+"</td>"
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

def ingredients_save(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0: # if is an update
            Ingredients.objects.filter(id=r['id']).update(title=r['title'], description=r['description'], price=r['price'], measureUnit=r['measureUnit'], ammount=r['ammount'])
            context = {
                'code': 1,
                'msg': 'Ingredient updated.',
            }
        else: # if is a new insert
            query = Ingredients(title=r['title'], description=r['description'], price=r['price'], measureUnit=r['measureUnit'], ammount=r['ammount'])
            query.save()
            context = {
                'code': 1,
                'msg': 'Ingredient saved.',
            }

    return JsonResponse(context)

def ingredients_delete(request):
    if request.method == "POST":
        r = request.POST
        if int(r['id']) > 0:
            Ingredients.objects.filter(id=r['id']).update(deleted=True)
            context = {
                'code': 1,
                'msg': 'Ingredient deleted.',
            }
        else:
            context = {
                'code': 1,
                'msg': 'Error.',
            }

    return JsonResponse(context)
