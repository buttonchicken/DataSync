from django.urls import path
from .views import *

urlpatterns = [
    path('register',CreateUserStripe.as_view()),
    path('update/<id>',UpdateUserStripe.as_view()),
    path('fetch',FetchStripeUsers.as_view()),
]