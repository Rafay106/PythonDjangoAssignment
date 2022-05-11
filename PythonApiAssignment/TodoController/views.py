from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from . models import TodoModel
from . serializers import TodoSerializer

# Create your views here.

def UrlsApi(request):
    if request.method == 'GET':
        context = {
            "POST   - login"       : "Login user",
            "GET    - logout"      : "Login user",
            "POST   - register"    : "Register new user",
            "GET    - getall"      : "Get all the todo items",
            "GET    - get/<id>"    : "Get single todo item",
            "PUT    - put/<id>"    : "Update single Todo item",
            "POST   - create"      : "Create new todo item",
            "DELETE - delete/<id>" : "Delete a todo item",
        }
    return JsonResponse(context, safe = False)

def TodoListApi(request):
    if request.user.is_anonymous:
        return HttpResponse("Unauthorized", status=401)
    #Get all the todo items
    if request.method == 'GET':
        todos = TodoModel.objects.all()
        todos_serializer = TodoSerializer(todos, many = True)
        return JsonResponse(todos_serializer.data, safe=False)
    return JsonResponse("Error", safe=False)

@csrf_exempt
def TodoApi(request, t_id=0):
    if request.user.is_anonymous:
        return HttpResponse("Unauthorized", status=401)

    if request.user.role == 'A':
        #Get single todo item
        if request.method == 'GET':
            try:
                todo = TodoModel.objects.get(id=t_id)
                todos_serializer = TodoSerializer(todo)
                return JsonResponse(todos_serializer.data, safe = False)
            except:
                return JsonResponse("Todo not found", safe=False)

        #Update single Todo item
        elif request.method == 'PUT':
            todo_data = JSONParser().parse(request)
            try:
                todo = TodoModel.objects.get(id=t_id)
                todo_serializer = TodoSerializer(todo, data=todo_data)
                if todo_serializer.is_valid():
                    todo_serializer.save()
                    return JsonResponse("Updated Successfully", safe=False)
                return JsonResponse("Failed to Update", safe=False)
            except:
                return JsonResponse("Object Not found", safe=False)

        #Create new todo item
        elif request.method == 'POST':
            todo_data = JSONParser().parse(request)
            todo_serializer = TodoSerializer(data=todo_data)
            if todo_serializer.is_valid():
                todo_serializer.save()
                return JsonResponse("Added Successfully", safe=False)
            return JsonResponse('Failed to Add', safe=False)

        #Delete a todo item
        elif request.method == 'DELETE':
            try:
                todo = TodoModel.objects.get(id=t_id)
                todo.delete()
                return JsonResponse("Deleted Successfully", safe=False)
            except:
                return JsonResponse("Object Not found", safe=False)
    else:
        return JsonResponse("You are not Admin", safe=False)

        