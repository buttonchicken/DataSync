from django.urls import path
from .views import *

urlpatterns = [
    path('register',CreateUserDB.as_view()),
    path('update/<id>',UpdateUserDB.as_view()),
    path('fetch',FetchLocalUsers.as_view()),
]