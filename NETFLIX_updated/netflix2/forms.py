from .models import Image,Users,Comment

from django import forms
from .models import Image

class UploadImageForm(forms.ModelForm):
    # You do not need an ImageField in the form since you're manually handling the file upload
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Image
        fields = ['image_name', 'description']  # These are the fields that you want to include

    def clean_image_data(self):
        image_file = self.cleaned_data.get('image_data')  # You won't need this here, handle in the view
        if image_file:
            max_size = 5 * 1024 * 1024  # 5 MB limit
            if image_file.size > max_size:
                raise forms.ValidationError("The image file is too large. Maximum size is 5 MB.")
        return image_file

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
