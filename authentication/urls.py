from django.urls import path

from .views import *

urlpatterns = [
    path('createUser',register),
    path('getAllUsers',getAllUsers),
    path('login',auth),
    path('logout',auth),
]