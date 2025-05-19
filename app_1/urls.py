from django.contrib import admin
from django.urls import path
from app_1 import views

# url dispatching
urlpatterns = [
    path('homepage/',views.homepage,name='homepage'),
    path('about/',views.about_us,name='aboutpage'),
    path('service/',views.services,name='servicepage'),
    path('contact/',views.contact_us,name='contactpage'),
    path('html-template/',views.html_template_org,name='htmlTemplate'),
    path('model-template/',views.template_added_model,name='htmlTemplate'),
    path('bootstrap/',views.bootstrap, name='bootstrap'),
    # path('submitform/',views.submitform, name="submitform"),
    path('crud/',views.marking, name='crud'),
    path('display/', views.display),
    path('delete/<int:id>/', views.delete,name='update'),
    path('update/<int:id>/', views.update,name='delete'),
    path('form/', views.userForm ,name='formpage'),

    path('upload/', views.upload_images, name='upload_images'),
    path('display_images/', views.display_images, name='display_images'),
    # path('display_image/', views.display_images, name='display_image'),
    path('like/<int:image_id>/', views.like_image, name='like_image'),

]