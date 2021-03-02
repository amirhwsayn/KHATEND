from django.db.models import ObjectDoesNotExist
from django.urls import path
from rest_framework import generics, status, exceptions
from rest_framework.response import Response

from .Functions import errorBuild, SendMail
from .Serializers import Serializer_Token, Serializer_Teacher
from .models import Teacher, Token
from .Permissons import PERM_CreateTecher
from rest_framework.views import APIView


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


class test(generics.ListAPIView):
    queryset = Teacher.objects.filter(Teacher_Id='asdadasd')

    serializer_class = Serializer_Teacher


urls = [
    path('ct', CreatToken.as_view()),
    path('rt', CreateTeacher.as_view()),
    path('test', test.as_view())
]
