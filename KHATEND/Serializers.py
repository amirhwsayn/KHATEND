from rest_framework import serializers

from .models import Teacher, Token


class Serializer_Teacher(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            'Teacher_Token',
            'Teacher_Id',
            'Teacher_Password',
            'Teacher_Email',
            'Teacher_Name',
            'Teacher_Description',
            # 'Teacher_ProfileImage',
            'Teacher_CreateDate',
        )
        # read_only_fields = ('Teacher_Token', 'Teacher_CreateDate',)


class Serializer_Token(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'Token_Token',
            'Token_User_Email',
            'Token_User_Id',
            'Token_User_Password'
        )
        read_only_fields = ('Token_Code', 'Token_IsVerified', 'Token_Token', 'Token_CreateDate')
