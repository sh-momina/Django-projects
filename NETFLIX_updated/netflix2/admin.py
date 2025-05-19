from django.contrib import admin
from .models import Image,Comment,Like,Users

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Image)
admin.site.register(Users)