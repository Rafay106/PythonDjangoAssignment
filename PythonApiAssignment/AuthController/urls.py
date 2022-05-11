from django.urls import re_path
from . views import *

urlpatterns = [
    re_path(r'^login$', LoginUser.as_view()),
    re_path(r'^logout$', LogoutUser.as_view()),
    re_path(r'^register$', RegisterUser.as_view()),
]