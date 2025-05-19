from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import about,contact,portfolio,marks_sheet
from .forms import modelform,djangoform,marksform

# Create your views here.
def homepage(request):
    return HttpResponse("This is home page ")

def about_us(request):
    return HttpResponse("This is about page ")

def services(request):
    return HttpResponse("This is service page ")

def contact_us(request):
    return HttpResponse("This is contact page ")


# def submitform(request):
#     try:
#         if request.method == "POST":
#             varr = request.POST.get('favcolour')
#             varr2 = request.POST.get('birthday')
#             varr3 = request.POST['appointment']
#     except:
#         pass
#     return HttpResponse(varr2)      # using action goes on url on submit form

# def userForm(request):
#     # django form store in fn variable and passed to html file as dictionary key
#     jform = djangoform
#     mform = modelform
#     data = {
#         'djangoform': jform,
#         'modelform': mform
#         }
#     try:
#         if request.method == "POST":
#             var = request.POST.get('favcolour')
#             var2 = request.POST.get('birthday')
#             var3 = request.POST['appointment']
#             name = request.POST.get('full_name')
#             email = request.POST.get('email')
#             number= request.POST.get('phone_number')
#             message = request.POST.get('message')
#             en = contact(full_name = name, email=email, phone_number=number, message=message)
#             en.save()
#             # OR
#             # var = str(request.GET['favcolour'])
#             # var2 = int(request.GET['birthday'])
#             # this data variable created and send, used in form.html as when submit still data not gone from input, but only for these defined here rest with refresh data gone
#             data = {
#                 'djangoform': jform,
#                 'modelform': mform,
#                 'colour': var,
#                 'birthday' : var2,
#                 'appointment' :var3
#             }
#     except:
#         pass
#     return render(request, 'app_1/forms.html',data)

def bootstrap(request):
    data={
        'title':'Bootstrap created'
    }
    return render(request,'app_1/index(bootstrap).html',data)


# now to show the model data added through admin panel on the html website, we calling that data in html template so we already have a function calling that file so we will now add queries in that to get data added through admin panel
# from app_1.models import about,contact
def html_template_org(request):
    data={
        'title':'HTML_template'
    }
    return render(request,'app_1/index(template_org).html',data)

def template_added_model(request):
    aboutAdminData = about.objects.all() # Fetching all records
    aboutAdminData = about.objects.all().order_by('-about_title')   # - represend desending and simple represent accending
    contactAdminData = contact.objects.all()
    portfolioAdminData = portfolio.objects.all()[:1]    # limit like we have 2 entries in admin for portfolio but it will get 1 and its gettinh 2 on main page as for loop for 2 models has been made

    # for a in aboutAdminData:     # To check the data in the console (optional)
    #     print(a)  
    # for a in contactAdminData:
    #     print(a.full_name)
    #     print(a.email)
    #     print(a.phone_number)

    data={
        'title':'HTML(model added)_template',
        'aboutAdminData': aboutAdminData,
        'contactAdminDta':contactAdminData,
        'portfolioAdminData':portfolioAdminData,
    }
    return render(request,'app_1/index(template).html',data)

def display(request):
    a = marksform()
    return render(request,'app_1/crud.html',{'a':a})

def marking(request):
    success = False
    if request.method == 'POST':
        form = marksform(request.POST)
        if form.is_valid:
            form.save()
            success = True
            form = marksform()
            data = marks_sheet.objects.all()
    else:
        form = marksform()
        data = marks_sheet.objects.all()

    return render(request, 'app_1/crud.html',{'form':form, 'success':success, 'data':data})

def delete(request,id=0):
    instance = marks_sheet.objects.get(id=id)
    instance.delete()
    return redirect('crud')

def update(request,id=0):
    if request.method =='POST':
        if id == 0:
            form = marksform(request.POST)
        else:
            student = marks_sheet.objects.get(pk=id)
            form = marksform(request.POST,student)
        if form.is_valid():
            form.save()
        return redirect('/crud')
    

def userForm(request):
    if request.method == 'POST':
        form = modelform(request.POST)
        if form.is_valid():
            form.save()  
    else:
        form = modelform()
    return render(request, 'app_1/forms.html', {'form': form})

from django.shortcuts import render, redirect
from .models import BinaryImage
import base64

# def upload_images(request):
#     if request.method == "POST":
#         group_name = request.POST['group_name']  # Retrieve group name from form
#         files = request.FILES.getlist('images')  # Get multiple uploaded files

#         for file in files:
#             binary_data = file.read()  # Read the file as binary
#             BinaryImage.objects.create(
#                 group_name=group_name,  # Store the group name for each image
#                 image_data=binary_data
#             )

#         return redirect('display_images')  # Redirect to the page to display the images

#     return render(request, 'app_1/upload_images.html')

# from django.shortcuts import render, redirect
# from .models import BinaryImage

# def upload_images(request):
#     if request.method == 'POST':
#         # Get the uploaded images and titles from the form
#         images = request.FILES.getlist('images')  # List of uploaded images
#         titles = request.POST['titles'].split(',')  # Comma-separated titles

#         # Check if the number of titles matches the number of images
#         if len(images) != len(titles):
#             return render(request, 'app_1/upload_images.html', {'error': 'The number of titles must match the number of images.'})

#         # Save each image with its title and user
#         for image_file, title in zip(images, titles):
#             image_data = image_file.read()  # Read image as binary data

#             # Save the image with the user and title
#             BinaryImage.objects.create(
#                 user=request.user,  # The currently authenticated user
#                 title=title.strip(),  # Clean up any extra spaces from the title
#                 image_data=image_data  # Save the binary image data
#             )

#         return redirect('app_1/display_images')  # Redirect to the image display page

#     return render(request, 'app_1/upload_images.html')




# def display_images(request):
#     images = BinaryImage.objects.all()  # Retrieve all images from the database

#     # Convert binary data to base64 for display in HTML
#     for image in images:
#         image.image_data = base64.b64encode(image.image_data).decode('utf-8')


#     # Group images by their group_name
#     grouped_images = {}
#     for image in images:
#         if image.group_name not in grouped_images:
#             grouped_images[image.group_name] = []
#         grouped_images[image.group_name].append(image)

#     return render(request, 'app_1/display_images.html', {'grouped_images': grouped_images})

from django.shortcuts import render, get_object_or_404, redirect
from .models import BinaryImage

def like_image(request, image_id):
    # Fetch the image object
    image = get_object_or_404(BinaryImage, id=image_id)
    
    # Handle like/dislike based on session data
    if 'liked' in request.session and request.session['liked'] == image.id:
        # If the image is liked, remove the like (dislike)
        image.likes -= 1
        request.session['liked'] = None  # Reset session for this image
    else:
        # If the image is not liked, add the like
        image.likes += 1
        request.session['liked'] = image.id  # Set session for this image as liked
    
    image.save()  # Save the updated like count
    return redirect('diaplay_images')  # Redirect to the image list page

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import BinaryImage

def upload_images(request):
    # Check if the user is authenticated, otherwise use a fallback user (e.g., first user in the database)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.first()  # Fallback to the first user in the database or create a guest user

    if request.method == 'POST':
        # Get the images and titles from the request
        images = request.FILES.getlist('images')  # List of uploaded images
        titles = request.POST.get('titles', '').split(',')  # Comma-separated titles

        # Ensure the number of titles matches the number of images
        if len(images) != len(titles):
            return render(request, 'app_1/upload_images.html', {'error': 'The number of titles must match the number of images.'})

        # Save each image with its respective title and user
        for image_file, title in zip(images, titles):
            image_data = image_file.read()  # Read image as binary data

            # Save the image in the database
            BinaryImage.objects.create(
                user=user,
                title=title.strip(),  # Clean up title
                image_data=image_data
            )

        return redirect('display_images')  # Redirect to the page displaying the uploaded images

    return render(request, 'app_1/upload_images.html')


def display_images(request):
    # Fetch all the images from the database
    images = BinaryImage.objects.all()
    for image in images:
        image.b64encoded_data = base64.b64encode(image.image_data).decode('utf-8')
    return render(request, 'app_1/display_images.html', {'images': images})


    







