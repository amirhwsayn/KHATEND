from django.core.exceptions import ObjectDoesNotExist
from django.urls import path
from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .Functions import errorBuild, SendMail
from .Permissons import PERM_CreateTecher, PERM_LoginTeacher
from .Serializers import Serializer_Token, Serializer_Teacher
from .models import Teacher, Token


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


class CreateTeacher(APIView):
    permission_classes = [PERM_CreateTecher]

    def get(self, request):
        token = Token.objects.get(Token_Token=request.headers['token'])
        id = token.Token_User_Id
        email = token.Token_User_Email
        password = token.Token_User_Password
        Teacher.objects.create(
            Teacher_Id=id,
            Teacher_Email=email,
            Teacher_Password=password
        )
        mdata = Teacher.objects.filter(Teacher_Id=id)
        ddata = Serializer_Teacher(mdata, many=True)
        return Response(ddata.data, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.NotAuthenticated):
            return errorBuild('کد وارد شده نا معتبر است')


class LoginTeacher(generics.ListAPIView):
    permission_classes = [PERM_LoginTeacher]
    serializer_class = Serializer_Teacher

    def get_queryset(self):
        return Teacher.objects.filter(Teacher_Id=self.request.data['id'], Teacher_Password=self.request.data['password'])

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.NotAuthenticated):
            return errorBuild("در خواست نا معتبر")
        if isinstance(exc,ObjectDoesNotExist):
            return errorBuild("رمز عبور یا نام کاربری اشتباه وارد شده")


class test(generics.ListCreateAPIView):
    queryset = Teacher.objects.filter(Teacher_Id='asdasdasdasd')
    serializer_class = Serializer_Teacher


urls = [
    path('ct', CreatToken.as_view()),
    path('rt', CreateTeacher.as_view()),
    path('lg', LoginTeacher.as_view()),
    path('test', test.as_view())
]
