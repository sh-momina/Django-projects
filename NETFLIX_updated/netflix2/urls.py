
from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'netflix2'

urlpatterns = [
    path('profile/',views.profile_view, name='profile'),
    path('upload_image/', views.upload_image_view, name='upload_image2'),
    path('delete_image/<int:image_id>/', views.delete_image_view, name='delete_image'),
    path('edit_image/<int:image_id>/', views.edit_image_view, name='edit_image'),
    path('all_images/', views.all_images_view, name='all_images'),
    path('image/<int:image_id>/add_comment/', views.add_comment_view, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),
    path('image/<int:image_id>/', views.view_image_view, name='view_image'),
    path('image/<int:image_id>/like_view/', views.like_view, name='like_view'),
]
