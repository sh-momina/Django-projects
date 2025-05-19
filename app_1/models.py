from django.db import models
# Create your models here.

class about(models.Model):
    about_icon=models.CharField(max_length=20)
    about_title=models.CharField(max_length=20)
    about_description=models.TextField()



class portfolio(models.Model):
    icon = models.CharField(max_length=20)
    heading = models.CharField(max_length=20)
    image = models.ImageField(upload_to='D:\study\Languages\Django\Django_project\project_with_harry')   
    #link where image is stored

class navbar(models.Model):
    nav_heading = models.CharField(max_length=70)
    nav_item1 = models.CharField(max_length=10)
    nav_item2 = models.CharField(max_length=10)

# creating django forms
class marks_sheet(models.Model):
    name = models.CharField(max_length=20)
    marks = models.IntegerField(default=0)

class contact(models.Model):
    full_name = models.CharField(max_length=50, name="full_name")
    email = models.EmailField(name="email")
    phone_number = models.CharField(max_length=11, name="phone_number")
    message = models.TextField(name="message")

# models.py
from django.db import models

class BinaryImage(models.Model):
    group_name = models.CharField(max_length=100, default='default_group')  # Field to store the group name
    image_data = models.BinaryField()  # Stores the image as binary data
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image in group: {self.group_name}"

# models.py
# from django.db import models
# from django.contrib.auth.models import User

# class BinaryImage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link image to user
#     title = models.CharField(max_length=255,default='Untitled')  # Store the title of the image
#     image_data = models.BinaryField()  # Store the image data in binary format
#     uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set the upload date
#     likes = models.IntegerField(default=0)  # Store the like count for the image

# models.py

from django.contrib.auth.models import User
from django.db import models

class BinaryImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate each image with a user
    title = models.CharField(max_length=255)  # Title for each image
    image_data = models.BinaryField()  # Store the image data in binary format
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the image is uploaded
    likes = models.IntegerField(default=0)  # To store likes for the image

    def __str__(self):
        return self.title
  


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(BinaryImage, on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'image')  # Ensures a user can like/dislike an image only once
