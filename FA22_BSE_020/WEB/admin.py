from django.contrib import admin
from . import models
from .models import student,student2,course,student_certificate,teacher_review,tempmodel,user, adddate,task,ImageModel

# Register your models here.
class studentadmin(admin.ModelAdmin):
    list_display = ('name','reg_number','email','message')
admin.site.register(student,studentadmin)

class student2admin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(student2,student2admin)

class certificate_admin(admin.ModelAdmin):
    list_display = ('certificate_name','certificate')
admin.site.register(student_certificate,certificate_admin)

class courseadmin(admin.ModelAdmin):
    list_display = ('name','course')
admin.site.register(course,courseadmin)

class reviewadmin(admin.ModelAdmin):
    list_display = ('studentbody','rating')
admin.site.register(teacher_review,reviewadmin)

class tempadmin(admin.ModelAdmin):
    list_display = ('name','reg_number','email','message')
admin.site.register(tempmodel,tempadmin)

class useradmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','username','password','confirm_password','contact','date_of_birth','gender','address','province')
admin.site.register(user,useradmin)

class dateadmin(admin.ModelAdmin):
    list_display = ('date',
                    )
admin.site.register(adddate,dateadmin)

class taskadmin(admin.ModelAdmin):
    list_display = ('select_date','task')
admin.site.register(task,taskadmin)

class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'mime_type','upload_date')
admin.site.register(ImageModel,ImageModelAdmin)