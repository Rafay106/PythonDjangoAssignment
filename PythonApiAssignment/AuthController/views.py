from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout

from . serializers import RegisterSerializer
from . models import UserModel

# Create your views here.

@csrf_exempt
def loginUser(request):
    if request.user.is_authenticated:
        return JsonResponse("You are loggined", safe=False)

    if request.method == 'POST':
        login_data = JSONParser().parse(request)
        e_name = login_data['email']
        p_word = login_data['password']
        print(f'\nEmail: {e_name}\nPassword: {p_word}')
        
        try:
            user = UserModel.objects.get(email=e_name)
        except:
            return JsonResponse("User not found", safe=False)
        user = authenticate(email=e_name, password=p_word)
        print(f'User: {user}\n')
        if user is not None:
            login(request, user)
            return JsonResponse("Successfully Logined", safe=False)
        else:
            return JsonResponse("Username or Password does not exist!", safe=False)
    return JsonResponse("Error", safe=False)

def logoutUser(request):
    if request.user.is_anonymous:
        return JsonResponse("Already logged out", safe=False)
    if request.method == 'GET':
        try:
            logout(request)
            return JsonResponse("Succesfully Logout", safe=False)
        except:
            return JsonResponse("Logout failed", safe=False)
    return JsonResponse("Error", safe=False)

@csrf_exempt
def registerUser(request):
    if not request.user.is_anonymous and request.user.role == 'A':
        if request.method == 'POST':
            login_data = JSONParser().parse(request)
            login_serializer = RegisterSerializer(data=login_data)
            if login_serializer.is_valid():
                login_serializer.save()
                return JsonResponse("User Created Successfully", safe=False)
            return JsonResponse("Failed to create user", safe=False)
        return JsonResponse("Error", safe=False)
    return JsonResponse("Unauthorized, Only admin can resgister new users.", safe=False)