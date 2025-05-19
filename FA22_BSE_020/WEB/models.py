from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
import base64
# from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    message = models.TextField()


class course(models.Model):
    courses = [
        ('en','english'),
        ('ur','urdu'),
        ('mt','maths'),
        ('sc','science'),
    ]
    name = models.CharField(max_length=50)
    course = models.CharField(max_length=4, choices=courses)

# one to many
class teacher_review(models.Model):
    rating = [
        ('1','best'),
        ('2','nice'),
        ('3','better'),
        ('4','wosrt'),
    ]
    studentbody = models.ForeignKey(course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(max_length=1, choices=rating)

    # many to many
class student2(models.Model):
    name = models.CharField(max_length=20)
    courses = models.ManyToManyField(course, related_name='students')

class student_certificate(models.Model):
    certificate = models.OneToOneField(student2, on_delete=models.CASCADE, related_name='certificate')
    certificate_name = models.CharField(max_length=50)


class tempmodel(models.Model):
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    
class user(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    PROVINCE_CHOICES = [
        ('punjab', 'Punjab'),
        ('sindh', 'Sindh'),
        ('kpk', 'Khyber Pakhtunkhwa'),
        ('balochistan', 'Balochistan'),
        ('gilgit_baltistan', 'Gilgit-Baltistan')
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])
    confirm_password = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class adddate(models.Model):
    date = models.DateField()
    
    def __str__(self):
        return str(self.date)

class task(models.Model):
    select_date = models.ForeignKey(adddate, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.select_date}"


class ImageModel(models.Model):
    image_name = models.CharField(max_length=100)
    image_data = models.BinaryField()         # Binary field to store image data
    mime_type = models.CharField(max_length=50)  # Field to store MIME type
    upload_date = models.DateTimeField(default=timezone.now)  # Field for upload timestamp

    def __str__(self):
        return self.image_name
    
    def get_image_base64(self):
        return base64.b64decode(self.image_data).decode('utf-8')



from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class CustomUser(AbstractUser):
    pass  # Using the built-in fields (username, email, password, etc.)


class Image(models.Model):
    post_id = models.CharField(max_length=255, null=True, blank=True)  # New field for grouping images
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    image_name = models.CharField(max_length=255)
    image_data = models.BinaryField()
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.image_name} by {self.user.username}"
    def get_image_base64(self):
        return base64.b64decode(self.image_data).decode('utf-8')
    def get_comments(self):
        return self.comments.all()

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user} on {self.image}'

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"Comment by {self.user.username} on {self.image.image_name}"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'image')  # Ensure each user can like an image only once

    def __str__(self):
        return f"{self.user.username} likes {self.image.image_name}"
    

