from django.db.models import ObjectDoesNotExist
from django.urls import path
from rest_framework import generics
from .Functions import errorBuild, SendMail
from .Serializers import Serializer_Token
from .models import Teacher


# Create your views here.

class CreatToken(generics.CreateAPIView):
    serializer_class = Serializer_Token

    def create(self, request, *args, **kwargs):
        id = request.data['Token_User_Id']
        email = request.data['Token_User_Email']
        try:
            Teacher.objects.get(Teacher_Id=id)
            return errorBuild('این نام کاربری قبلا انتخاب شده')
        except ObjectDoesNotExist:
            try:
                Teacher.objects.get(Teacher_Email=email)
                return errorBuild('این پست الکترونیکی قبلا انتخاب شده')
            except ObjectDoesNotExist:
                return super().create(request, args, kwargs)

    def perform_create(self, serializer):
        obj = serializer.save()
        SendMail(obj.Token_Code, obj.Token_User_Email)


urls = [
    path('ct', CreatToken.as_view()),
]
