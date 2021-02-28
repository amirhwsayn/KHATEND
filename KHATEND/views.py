from django.urls import path
from rest_framework import generics
from .Serializers import Serializer_Token


# Create your views here.

class CreatToken(generics.CreateAPIView):
    serializer_class = Serializer_Token


urls = [
    path('ct', CreatToken.as_view())
]
