from django.db import models
from .Randoms import Random_Token, Random_Name, Random_Code


# Create your models here.

class Teacher(models.Model):
    Teacher_Token = models.TextField(max_length=100, unique=True, default=Random_Token)
    Teacher_Id = models.CharField(max_length=50, unique=True)
    Teacher_Password = models.CharField(max_length=50)
    Teacher_Email = models.EmailField(unique=True)
    Teacher_Name = models.CharField(max_length=50, default=Random_Name)
    Teacher_Description = models.TextField(max_length=300, blank=True)
    Teacher_ProfileImage = models.FileField(upload_to='image/', blank=True, default='image/iconfinder_1041_boy_c_2400506.png')
    Teacher_CreateDate = models.DateTimeField(auto_now=True)


class Token(models.Model):
    # Token Data
    Token_Token = models.TextField(max_length=100, unique=True, default=Random_Token)
    Token_Code = models.CharField(max_length=6, default=Random_Code)
    Token_IsVerified = models.BooleanField(default=False)
    Token_CreateDate = models.DateTimeField(auto_now=True)
    # User Data
    Token_User_Email = models.EmailField()
    Token_User_Id = models.CharField(max_length=50)
    Token_User_Password = models.CharField(max_length=50)
