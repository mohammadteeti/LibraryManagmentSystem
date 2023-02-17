from django.contrib import admin
from .models import Student,Book,IssuedBook
# Register your models here.

admin.site.register(Student)
admin.site.register(Book)
admin.site.register(IssuedBook)
