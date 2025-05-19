
from django.urls import path
from WEB import views

urlpatterns = [
    path('courses/',views.index),
    path('crud2/',views.crud2, name='crud2'),
    path('crud/',views.crud, name='crud'),
    path('add/',views.add, name="add"),
    path('delete/<int:id>',views.delete,name='delete'),
    path('update/<int:id>',views.update,name='update'),
    path('add2/',views.add2, name="add2"),

    path('user/',views.users, name="userdata"),
    path('alluser/',views.allusers, name="alluser"),
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    path('update_user/<int:id>',views.update_user,name='update_user'),

    path('date/',views.add_date, name="add_date"),
    path('task/',views.add_task, name="add_task"),
    path('alltask/',views.all_tasks, name="all_task"),
    path('delete_task/<int:id>',views.delete_task,name='delete_task'),
    path('update_task/<int:id>',views.update_task,name='update_task'),


    path('upload/', views.upload_image, name='upload_image'),
    path('images/', views.image_list, name='image_list'),  # URL for the list view
    path('images/<int:image_id>/', views.image_detail, name='image_detail'),  # URL for the detail view
    path('display/<int:image_id>/', views.display_image, name='display_image'),  # URL to serve the image data

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('upload_image/', views.upload_image_view, name='upload_image2'),
    path('delete_image/<int:image_id>/', views.delete_image_view, name='delete_image'),
    path('edit_image/<int:image_id>/', views.edit_image_view, name='edit_image'),
    path('all_images/', views.all_images_view, name='all_images'),
    path('image/<int:image_id>/add_comment/', views.add_comment_view, name='add_comment'),
    path('image/<int:image_id>/add_comment/<int:parent_comment_id>/', views.add_comment_view, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),
    path('image/<int:image_id>/', views.view_image_view, name='view_image'),
    path('image/<int:image_id>/like_view/', views.like_view, name='like_view'),
]

    



