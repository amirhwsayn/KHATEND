from django.contrib import admin
from .models import Teacher, Token

# Register your models here.
admin.site.register(Teacher, Token)
