from django.contrib import admin

from lib_manage.models import Book, UserGetBooks, UserReg

# Register your models here.
admin.site.register(Book)
admin.site.register(UserReg)
admin.site.register(UserGetBooks)
