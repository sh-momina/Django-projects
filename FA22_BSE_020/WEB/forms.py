from django import forms
from .models import student,student2,student_certificate,teacher_review,course,tempmodel,user,adddate,task
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class studentform(forms.ModelForm):
    class Meta:
        model = student
        fields = ['name','reg_number','email','message']

class student2form(forms.ModelForm):
    class Meta:
        model = student2
        fields = ['name','courses']

class reviewform(forms.ModelForm):
    class Meta:
        model = teacher_review
        fields = ['studentbody','rating']

class certificateform(forms.ModelForm):
    class Meta:
        model = student_certificate
        fields = ['certificate','certificate_name']

class courseform(forms.ModelForm):
    class Meta:
        model = course
        fields = ['name','course']

class tempform(forms.ModelForm):
    class Meta:
        model = student
        fields = ['name','reg_number','email','message']

class userform(forms.ModelForm):
    class Meta:
        model = user
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password', 'confirm_password',
            'contact', 'date_of_birth', 'gender', 'address', 'province',
        ]
        widgets = {
            'gender': forms.RadioSelect(choices=user.GENDER_CHOICES),  # Radio buttons for gender
            'province': forms.Select(choices=user.PROVINCE_CHOICES),   # Dropdown for province
        }

class dateform(forms.ModelForm):
    class Meta:
        model = adddate
        fields = ['date']

class taskform(forms.ModelForm):
    class Meta:
        model = task
        fields = ['select_date','task']

class ImageUploadForm(forms.Form):
    image = forms.ImageField()  # ImageField to receive the image file from the user

# class SignupForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password1', 'password2']

# class LoginForm(AuthenticationForm):
#     pass

# class ImageUploadForm2(forms.ModelForm):
#     image_file = forms.ImageField(required=True)  # New field for uploading images

#     class Meta:
#         model = ImageModel2
#         fields = ['image_file']  # Include only the upload field

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Image,CustomUser,Comment
# from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UploadImageForm(forms.ModelForm):
    # image = forms.ImageField()
    class Meta:
        model = Image
        fields = []


class LoginForm(AuthenticationForm):
    pass

from django import forms
from .models import Image

class EditImageForm(forms.ModelForm):
    image = forms.ImageField(required=True)  # Allow replacing the image (optional)

    class Meta:
        model = Image
        fields = ['image_name','image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']  # Include parent to enable nested replies
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'parent': forms.HiddenInput(),  # Hide the parent field by default
        }




        