from django.contrib import admin
from .models import UserModel, Address, BlogModel

admin.site.register(UserModel)
admin.site.register(Address)
admin.site.register(BlogModel)
