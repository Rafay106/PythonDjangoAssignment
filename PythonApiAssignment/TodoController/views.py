from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, exceptions as ex
from jwt import exceptions
import jwt

from AuthController.models import UserModel

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
    return Response(context)

#Get all the todo items
class TodoListApi(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise ex.NotAuthenticated("Login required")
        todos = TodoModel.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

class TodoApi(APIView):
    # This method returns True or False depending on the role of authenticated user
    # If user is not authicated or logged in then it raises exceptions.
    def authUser(self, request):
        token = request.COOKIES.get('jwt')
        role = None
        if token is None:
            raise ex.NotAuthenticated("Login required")
        else:
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                try:
                    user = UserModel.objects.get(email=payload['email'])
                    role = user.role
                except:
                    raise ex.ValidationError("Invalid token")
            except jwt.ExpiredSignatureError:
                raise exceptions.ExpiredSignatureError("Payload expired")
        # Checking the role of user
        if role == 'A':
            return True
        return False

    #Get single todo item
    def get(self, request, t_id):
        # If user has Admin role
        if self.authUser(request):
            try:
                todo = TodoModel.objects.get(id=t_id)
                serializer = TodoSerializer(todo)
                return Response(serializer.data)
            except:
                return Response({"Error" : "Todo not found"})
        return Response({"HTTP 401" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    #Update single Todo item
    def put(self, request, t_id):
        # If user has Admin role
        if self.authUser(request):
            try:
                todo = TodoModel.objects.get(id=t_id)
                serializer = TodoSerializer(todo, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"message" : "Updated Successfully"})
            except:
                return Response({"message" : "Object Not found"})
        return Response({"HTTP 401" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    #Create new todo item
    def post(self, request):
        # If user has Admin role
        if self.authUser(request):
            serializer = TodoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message" : "Created Successfully"})
        return Response({"HTTP 401" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    #Delete a todo item
    def delete(self, request, t_id):
        # If user has Admin role
        if self.authUser(request):
            try:
                todo = TodoModel.objects.get(id=t_id)
                todo.delete()
                return Response({"message" : "Deleted Successfully"})
            except:
                return Response({"message" : "Todo not found"})
        return Response({"HTTP 401" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
