from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadImageForm, EditImageForm, CommentForm
from .models import Image, Like, Comment
import base64

def delete_image_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('/all_images/')

def edit_image_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        form = EditImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            if 'image' not in request.FILES:
                form.instance.image_data = image.image_data
            form.save()
            return redirect('/all_images/')
    else:
        form = EditImageForm(instance=image)

    return render(request, 'netflix2/edit_image.html', {'form': form, 'image': image})

def profile_view(request):
    images = Image.objects.all()
    for image in images:
        image.b64_data = base64.b64encode(image.image_data).decode('utf-8')

    return render(request, 'netflix2/profile.html', {'images': images})

from django.shortcuts import render, redirect
from .forms import UploadImageForm
from .models import Image

def upload_image_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the image file upload manually
            image_file = request.FILES.get('image_data')  # 'image_data' is the name of the input field for image

            if image_file:
                # Check if the image size is acceptable
                max_size = 5 * 1024 * 1024  # 5 MB limit
                if image_file.size > max_size:
                    form.add_error('image_data', 'Image file is too large. Max size is 5MB.')
                    return render(request, 'netflix2/upload_image2.html', {'form': form})

                # Create a new Image instance with the form data
                image = form.save(commit=False)  # Don't save to the database yet
                image.image_data = image_file.read()  # Store the image as binary data in image_data
                image.save()  # Save the instance to the database
                return redirect('netflix2:profile')  
            else:
                form.add_error('image_data', 'No image file uploaded.')  # Handle case where no file is uploaded
        else:
            form.add_error('image_data', 'Form is not valid.')
    else:
        form = UploadImageForm()

    return render(request, 'netflix2/upload_image2.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
import base64
from .models import Image, Comment
from .forms import CommentForm

def all_images_view(request):
    images = Image.objects.all()
    # Encode image data to base64 for display
    for image in images:
        image.b64_data = base64.b64encode(image.image_data).decode('utf-8')
    return render(request, 'netflix2/all_images.html', {'images': images})

def add_comment_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = None  # No authentication, set to None or default
            comment.save()
            return redirect('all_images')
    else:
        form = CommentForm()

    return render(request, 'netflix2/add_comment.html', {'form': form, 'image': image})


def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('all_images')  # Redirect to the page displaying all images and comments


def view_image_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    comments = image.comments.all()
    return render(request, 'netflix2/all_images.html', {'image': image, 'comments': comments})


def like_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    like, created = Like.objects.get_or_create(user=None, image=image)  # Set user to None
    if not created:
        like.delete()  # If the like exists, remove it (undo the like)
    return redirect('all_images')  # Redirect to all images page (or wherever you want)
