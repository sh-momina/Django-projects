from django.contrib import admin
from app_1.models import about,marks_sheet
from app_1.models import contact,portfolio
from . import models
from .models import marks_sheet
# Register your models here.

# another way to register 
# from . import models
# admin.site.register(models.contact)

admin.site.register(models.navbar)

class marks_admin(admin.ModelAdmin):
    list_display= ('name','marks')
admin.site.register(marks_sheet,marks_admin)

class about_admin(admin.ModelAdmin):
    list_display=('about_icon','about_description','about_title')

admin.site.register(about,about_admin)



class portfolio_admin(admin.ModelAdmin):
    list_display = ('icon','heading','image')

admin.site.register(portfolio,portfolio_admin)


class contact_admin(admin.ModelAdmin):
    list_display = ('full_name','email','phone_number','message')

admin.site.register(contact,contact_admin)

