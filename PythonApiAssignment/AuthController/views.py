from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
import jwt, datetime

from . serializers import UserSerializer
from . models import UserModel

# Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginUser(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = UserModel.objects.get(email=email)
        except:
            raise exceptions.AuthenticationFailed("User Not Found!")
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect Password!")
            
        payload = {
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'email'     : user.email,
            'is_active' : user.is_active,
            'role'      : user.role,
            'exp'       : datetime.datetime.utcnow() + datetime.timedelta(minutes=600),
            'iat'       : datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True, max_age=36000)
        response.data = {
            "jwt" : token
        }
        return response

class LogoutUser(APIView):
    def post(self, request):
        if request.COOKIES.get('jwt') is not None:
            response = Response()
            response.delete_cookie('jwt')
            response.data = {
                "message" : "Successfully logged out."
            }
            return response
        else:
            return Response(
                {"message" : "Already logged out"}
            )