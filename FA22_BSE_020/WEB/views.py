from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from .models import student,student2,student_certificate,teacher_review,course,tempmodel,user,adddate,task,ImageModel
from .forms import studentform,student2form,courseform,reviewform,certificateform,tempform,userform,dateform,taskform,ImageUploadForm
import mimetypes  # To detect MIME types

# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
# from .forms import SignupForm, LoginForm, ImageUploadForm2
# from .models import ImageModel2

def index(request):
    return render(request,'WEB/index.html')

# def crud2(request):
#     data ={
#         'student':student2.objects.all(),
#         'review':teacher_review.objects.all(),
#         'cert':student_certificate.objects.all(),
#         'course':course.objects.all()
#     }
#     return render(request,'WEB/crud2.html',data)

# def add2(request):
#     if request.method == 'POST':
#         stu_form = student2form(request.POST)
#         review_form = reviewform(request.POST)
#         cert_form = certificateform(request.POST)
#         sub_form = courseform(request.POST)
#         if stu_form.is_valid() or review_form.is_valid() or cert_form.is_valid() or sub_form.is_valid():
#             stu_form.save()
#             review_form.save()
#             cert_form.save()
#             sub_form.save()
#             stu_form = student2form()
#             review_form = reviewform()
#             cert_form = certificateform()
#             sub_form = courseform()
#             return redirect('/crud2/')
#     else:
#         stu_form = student2form()
#         review_form = reviewform()
#         cert_form = certificateform()
#         sub_form = courseform()

#         return render(request,'WEB/crud2.html',{'stu_form':stu_form, 'review_form':review_form, 'cert_form':cert_form, 'sub_form':sub_form})


def crud2(request):
    # Initialize forms
    stu_form = student2form()
    review_form = reviewform()
    cert_form = certificateform()
    sub_form = courseform()
    
    # Prepare the data for both the forms and the tables
    data = {
        'stu_form': stu_form,
        'review_form': review_form,
        'cert_form': cert_form,
        'sub_form': sub_form,
        'student': student2.objects.all(),
        'review': teacher_review.objects.all(),
        'cert': student_certificate.objects.all(),
        'course': course.objects.all()
    }
    
    return render(request, 'WEB/crud2.html', data)

# View for handling form submission (POST request)
def add2(request):
    if request.method == 'POST':
        stu_form = student2form(request.POST)
        review_form = reviewform(request.POST)
        cert_form = certificateform(request.POST)
        sub_form = courseform(request.POST)
        
        # Check if the forms are valid and save the data
        if stu_form.is_valid():
            stu_form.save()
        if review_form.is_valid():
            review_form.save()
        if cert_form.is_valid():
            cert_form.save()
        if sub_form.is_valid():
            sub_form.save()
        
        # Redirect back to the crud2 page after successful submission
        return redirect('crud2')
    
    else:
        # In case of GET request, redirect to the main page
        return redirect('crud2')


def temp(request):
    return render(request,'WEB/temp.html',{'data':tempmodel.objects.all()})


def crud(request):
    return render(request,'WEB/crud.html',{'data':student.objects.all()})

def add(request):
    if request.method == "POST":
        form = studentform(request.POST)
        if form.is_valid():
            form.save()
            form = studentform()
            return redirect('/crud/')
    else:
        form = studentform()

    return render(request,'WEB/add_data.html',{'form':form})

def delete(request, id):
    data = get_object_or_404(student, id=id)
    # data = student.objects.all(pk=reg_number)
    data.delete()
    return redirect('/crud/')

def update(request, id):
    data = get_object_or_404(student, id=id)
    if request.method == 'POST':
        form = studentform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('/crud/')
    else:
        form = studentform(instance=data)
    return render(request,'WEB/update.html',{'form':form, 'data':data})

def users(request):
    if request.method == "POST":
        form = userform(request.POST)
        if form.is_valid():
            form.save()
            form = userform()
            return redirect('userdata')
    else:
        form = userform()
    return render(request,'WEB/user_data.html',{'form':form})

def allusers(request):
    return render(request,'WEB/display_users.html',{'data':user.objects.all()})

def delete_user(request, id):
    data = get_object_or_404(user, id=id)
    data.delete()
    return redirect('/alluser/')

def update_user(request, id):
    data = get_object_or_404(user, id=id)
    if request.method == 'POST':
        form = userform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('/alluser/')
    else:
        form = userform(instance=data)
    return render(request,'WEB/update_user.html',{'form':form, 'data':data})


def add_date(request):
    if request.method == "POST":
        form = dateform(request.POST)
        if form.is_valid():
            form.save()
            form = dateform()
            return redirect('add_date')
    else:
        form = dateform()
    return render(request,'WEB/add_date.html',{'form':form})

def add_task(request):
    if request.method == "POST":
        form2 = taskform(request.POST)
        if form2.is_valid():
            form2.save()
            form2 = taskform()
            return redirect('add_date')
    else:
        form2 = taskform()
    return render(request,'WEB/task.html',{'form2':form2})

def all_tasks(request):
    return render(request,'WEB/all_tasks.html',{'data':task.objects.all()})

def delete_task(request, id):
    data = get_object_or_404(task, id=id)
    data.delete()
    return redirect('/alltask/')

def update_task(request, id):
    data = get_object_or_404(task, id=id)
    if request.method == 'POST':
        form = taskform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('/alltask/')
    else:
        form = taskform(instance=data)
    return render(request,'WEB/update_task.html',{'form':form, 'data':data})


# View for uploading images
def upload_image(request):
    image = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            binary_data = image_file.read()
            mime_type, _ = mimetypes.guess_type(image_file.name)

            # Save the binary data and MIME type in the database
            image = ImageModel.objects.create(
                image_name=image_file.name,
                image_data=binary_data,
                mime_type=mime_type or 'application/octet-stream'  # Default if MIME type is unknown
            )

            return redirect('upload_image')
    else:
        form = ImageUploadForm()
    return render(request, 'WEB/upload_extend.html', {'form': form, 'image': image})

# View to list all images
def image_list(request):
    images = ImageModel.objects.all()
    return render(request, 'WEB/image_list.html', {'images': images})

# View to display individual image details
def image_detail(request, image_id):
    image = ImageModel.objects.get(id=image_id)
    return render(request, 'WEB/image_detail.html', {'image': image})

# View to serve image data
def display_image(request, image_id):
    image_record = ImageModel.objects.get(id=image_id)
    return HttpResponse(image_record.image_data, content_type=image_record.mime_type)


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, UploadImageForm,EditImageForm,CommentForm
from .models import Image,Like
import base64
from django.urls import reverse
from django.views.generic import ListView
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import uuid


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile/')
    else:
        form = SignupForm()
    return render(request, 'WEB/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/profile/')
    else:
        form = LoginForm()
    return render(request, 'WEB/login.html', {'form': form})

@login_required
def delete_image_view(request, image_id):
    # Get the image object for the logged-in user
    image = get_object_or_404(Image, id=image_id, user=request.user)
    image.delete()
    return redirect('/all_images/')

@login_required
def edit_image_view(request, image_id):
    image = get_object_or_404(Image, id=image_id, user=request.user)

    if request.method == 'POST':
        form = EditImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            if 'image' not in request.FILES:
                form.instance.image_data = image.image_data
            form.save()
            return redirect('/all_images/')  # Adjust the redirect as needed
    else:
        form = EditImageForm(instance=image)

    return render(request, 'WEB/edit_image.html', {'form': form, 'image': image})

@login_required
def profile_view(request):
    images = Image.objects.filter(user=request.user)
    # Encode image data to base64
    for image in images:
        image.b64_data = base64.b64encode(image.image_data).decode('utf-8')
    # Pass the base64-encoded image data (b64_data) to the template
    # print(f"Number of images passed to the template: {len(images)}")
    return render(request, 'WEB/profile.html', {'images': images})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadImageForm, CommentForm
from .models import Image,Comment

@login_required
def upload_image_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST)
        if form.is_valid():
            image_files = request.FILES.getlist('image_data')  # Get all uploaded files
            image_titles = request.POST.getlist('image_titles')  # Get all titles from the form

            # Check if the number of titles matches the number of images
            if len(image_files) != len(image_titles):
                form.add_error(None, 'The number of titles must match the number of images uploaded.')
                return render(request, 'WEB/upload_image2.html', {'form': form})

            # Iterate through each file and title pair
            for index, image_file in enumerate(image_files):
                title = image_titles[index]
                # Save each image with the corresponding title
                image = Image(
                    user=request.user,
                    image_data=image_file.read(),  # Save image binary data
                    image_name=title,
                )
                image.save()

            return redirect('/profile/')
        else:
            return render(request, 'WEB/upload_image2.html', {'form': form})
    else:
        form = UploadImageForm()

    return render(request, 'WEB/upload_image2.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login/')

def all_images_view(request):
        images = Image.objects.all()
        # images = Image.objects.filter(post_id="unique_post_id")
        for image in images:
            image.b64_data = base64.b64encode(image.image_data).decode('utf-8')
        return render(request, 'WEB/all_images.html', {'images': images})

def add_comment_view(request, image_id, parent_comment_id=None):
    image = get_object_or_404(Image, id=image_id)
    parent_comment = None

    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.parent = parent_comment
            comment.save()
            return redirect('all_images')
    else:
        form = CommentForm(initial={'parent': parent_comment_id})

    return render(request, 'WEB/add_comment.html', {'form': form, 'image': image, 'parent_comment': parent_comment})

def view_image_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    comments = image.comments.all()
    return render(request, 'WEB/all_images.html', {'image': image, 'comments': comments})

@login_required
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the comment belongs to the logged-in user or the image belongs to the user
    if comment.user == request.user or comment.image.user == request.user:
        comment.delete()
        return redirect('all_images')  # Redirect to the page displaying all images and comments
    else:
        # Handle the case where a user tries to delete someone else's comment
        return redirect('all_images')

# def view_image_view(request, image_id):
#     image = get_object_or_404(Image, id=image_id)

#     # Fetch only top-level comments (no parent)
#     top_level_comments = image.comments.filter(parent__isnull=True).prefetch_related('replies')

#     return render(request, 'WEB/view_image.html', {
#         'image': image,
#         'top_level_comments': top_level_comments
#     })

@login_required
def like_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    # Check if the user has already liked the image
    like, created = Like.objects.get_or_create(user=request.user, image=image)
    if not created:
        like.delete()  # If the like exists, remove it (undo the like)
    return redirect('all_images')  # Redirect to all images page (or wherever you want)

