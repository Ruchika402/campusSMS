from django.contrib import admin

# Register your models here.

from .models import Student, ClassRoom

admin.site.register(Student)

admin.site.register(ClassRoom)
