from django.urls import re_path
from . views import *

urlpatterns = [
    re_path(r'^$', UrlsApi.as_view()),

    re_path(r'^getall$', TodoListApi.as_view()),
    
    re_path(r'^get/(?P<t_id>[0-9]+)$', TodoApi.as_view()),
    re_path(r'^put/(?P<t_id>[0-9]+)$', TodoApi.as_view()),
    re_path(r'^create$', TodoApi.as_view()),
    re_path(r'^delete/(?P<t_id>[0-9]+)$', TodoApi.as_view()),
]