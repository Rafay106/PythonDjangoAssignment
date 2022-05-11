from django.urls import re_path
from . views import *

urlpatterns = [
    re_path(r'^login$', loginUser),
    re_path(r'^logout$', logoutUser),
    re_path(r'^register$', registerUser),
]