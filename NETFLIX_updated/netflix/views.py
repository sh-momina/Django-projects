from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password  # To hash passwords
from .forms import MovieForm, UserForm,ProfileForm,ComplaintForm,top_ten,EpisodeForm,SeasonForm
from .models import Users,Languages,Faq,Complaint,TopTenMovies,Episode,Season
from django.shortcuts import render, redirect
import base64
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.hashers import check_password
from .models import AppMovie,HorrorMovies
import stripe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Users
from .forms import LoginForm,HorrorForm
from django.views.decorators.csrf import csrf_protect

import base64
from django.shortcuts import render
from .models import AppMovie, HorrorMovies
from django.db import models
import json 

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def index(request):
    return render(request, 'netflix/index.html')

from django.shortcuts import render

from django.shortcuts import render
from django.urls import reverse

def help_page(request):
    # Retrieve FAQs from the database
    faqs = Faq.objects.all()

    # Get the redirect_url parameter from the request
    redirect_url = request.GET.get('redirect_url', reverse('home'))  # Default to 'home'

    # Validate the redirect_url against allowed patterns
    allowed_urls = [
        reverse('home'),
        reverse('home_basic'),
        reverse('home_mobile'),
        reverse('home_standard'),
        reverse('home_premium'),
    ]
    if redirect_url not in allowed_urls:
        redirect_url = reverse('home')  # Fallback to 'home' if invalid

    # Determine the type of home based on redirect_url
    home_type_map = {
        reverse('home'): 'Default Home',
        reverse('home_basic'): 'Basic Home',
        reverse('home_mobile'): 'Mobile Home',
        reverse('home_standard'): 'Standard Home',
        reverse('home_premium'): 'Premium Home',
    }
    home_type = home_type_map.get(redirect_url, 'Default Home')

    # Pass the validated redirect_url and home_type to the template
    context = {
        'faqs': faqs,
        'redirect_url': redirect_url,
        'home_type': home_type,
    }

    return render(request, 'netflix/help.html', context)

def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            if request.user.is_authenticated:
                complaint.user = request.user  # Assign the logged-in user to the complaint
            else:
                complaint.user = None  # Handle the case for anonymous users
            complaint.save()
            return redirect('help_page')  # Redirect to the help page after submission
    else:
        form = ComplaintForm()
    
    return render(request, 'netflix/submit_complaint.html', {'form': form})

class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        if email:
            request.session['email'] = email  
            return render(request, 'netflix/signup1.html', {'email': email}) 
        else:
            messages.error(request, "Email is required.")
            return render(request, 'netflix/signup.html')
    else:
        return render(request, 'netflix/signup.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
import stripe
import json

# Stripe API key
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

SUBSCRIPTION_PLANS = {
    "Mobile": 25000,    
    "Basic": 45000,     
    "Standard": 80000,  
    "Premium": 110000   
}
@csrf_protect
def process_payment(request):
    if request.method == "POST":
        try:
            print("Processing payment...")

            # Parse JSON data from the request body
            data = json.loads(request.body)
            print(f"Received data: {data}")

            # Extract fields from the data
            payment_method_id = data.get("payment_method_id")
            selected_plan = data.get("plan")
            customer_email = data.get("email")  

            print(f"Parsed values - Payment Method ID: {payment_method_id}, Plan: {selected_plan}, Email: {customer_email}")

            # Validate required fields
            if not all([payment_method_id, selected_plan, customer_email]):
                print("Missing required fields.")
                return JsonResponse({"error": "Missing required fields."}, status=400)

            # Validate the selected plan
            if selected_plan not in SUBSCRIPTION_PLANS:
                print("Invalid subscription plan.")
                return JsonResponse({"error": "Invalid subscription plan."}, status=400)

            # Calculate the amount for the selected plan
            amount = SUBSCRIPTION_PLANS[selected_plan]
            print(f"Amount for {selected_plan} plan: {amount}")

            # Create or retrieve a Stripe Customer
            customer = stripe.Customer.create(
                email=customer_email,
                payment_method=payment_method_id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
            )
            print(f"Created/Retrieved Stripe Customer: {customer}")

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="pkr",
                customer=customer.id,
                payment_method=payment_method_id,
                off_session=True,  
                confirm=True,      
                description=f"{selected_plan} Plan Subscription",
            )
            print(f"Stripe PaymentIntent response: {intent}")

            # Check the status of the PaymentIntent
            if intent['status'] == 'succeeded':
                print("Payment succeeded.")

                # Save the selected plan to the session
                request.session['selected_plan'] = selected_plan

                # Redirect to the success page
                return JsonResponse({"redirect_url": "/netflix/subscribed.html"}, status=200)

            print(f"Payment failed. Intent status: {intent['status']}")
            return JsonResponse({"error": f"Payment failed. Status: {intent['status']}"}, status=400)

        except stripe.error.CardError as e:
            print(f"Card error: {e.user_message}")
            return JsonResponse({"error": f"Card error: {e.user_message}"}, status=400)
        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            return JsonResponse({"error": f"Stripe error: {str(e)}"}, status=500)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    print("Invalid request method.")
    return JsonResponse({"error": "Invalid request method."}, status=400)

def signup_step2(request):
    if request.method == 'POST':
        email = request.session.get('email')  
        password = request.POST.get('password')  
        if email and password:
            request.session['password'] = password 
            return render(request, 'netflix/signup2.html', {'email': email})  
        else:
            messages.error(request, "Password is required.")
            return render(request, 'netflix/signup1.html', {'email': email})
    else:
        return redirect('signup')  

def signup3(request):
    return render(request, 'netflix/signup3.html') 

def save_subscription_and_payment(request):
    if request.method == 'POST':
        # Step 1: Retrieve data from session and form
        email = request.session.get('email')  
        password = request.session.get('password')  
        plan = request.POST.get('plan')  

        if email and password and plan:
            # Step 2: Save subscription data (Replace this with actual database saving logic)
            print(f"Email: {email}, Password: {password}, Plan: {plan}")

            # Step 3: Handle payment logic (Replace with actual payment integration)
            payment_status = process_payment(plan)  

            if payment_status:  
                messages.success(request, "Subscription and payment completed successfully!")
                return redirect('signup3') 
            else:
                messages.error(request, "Payment failed. Please try again.")
                return redirect('signup2')  
        else:
            messages.error(request, "An error occurred. Please try again.")
            return redirect('signup2')  
    else:
        return redirect('signup2')  

def subscribed(request):
    if request.method in ['POST', 'GET']:
        # Retrieve email, password, and plan from the session
        email = request.session.get('email')
        password = request.session.get('password')
        selected_plan = request.session.get('selected_plan')  # Added

        print(f"DEBUG: Session Email: {email}, Password: {password}, Plan: {selected_plan}")

        if email and password and selected_plan:  # Updated condition
            form_data = {'email': email, 'password_hash': password}
            form = UserForm(form_data)

            if form.is_valid():
                password = form.cleaned_data['password_hash']
                hashed_password = make_password(password)

                user = form.save(commit=False)
                user.password_hash = hashed_password
                user.save()

                request.session['user_id'] = user.user_id
                user = Users.objects.get(email=email)
                user.subscription_plan = selected_plan
                user.save()
                messages.success(request, "Payment successful! Subscription activated.")
                return render(request, 'netflix/subscribed.html', {
                    'email': email,
                    'plan': selected_plan
                })
            else:
                print("DEBUG: Form validation failed:", form.errors)
                messages.error(request, "Invalid data. Payment could not be processed.")
                return redirect('signup')

        print("DEBUG: Email, password, or plan missing in session.")
        messages.error(request, "Payment failed. Please try again.")
        return redirect('signup')

    print("DEBUG: Invalid request method.")
    return redirect('signup')

def profile_mobile(request):
    return render(request, 'netflix/profile_mobile.html')

def profile_basic(request):
    return render(request, 'netflix/profile_basic.html')  

def profile_standard(request):
    return render(request, 'netflix/profile_standard.html')

def profile_premium(request):
    return render(request, 'netflix/profile_premium.html')

def home_mobile(request):
    movies = AppMovie.objects.all()
    hmovies = HorrorMovies.objects.all()
    tmovies = TopTenMovies.objects.all()
    season = Season.objects.all()
    
    # Encoding movie image and video to base64
    for movie in movies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in hmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in tmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in season:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    return render(request, 'netflix/home_mobile.html', {'movies': movies, 'hmovies': hmovies, 'tmovies':tmovies,'season':season})

def home_basic(request):
    movies = AppMovie.objects.all()
    hmovies = HorrorMovies.objects.all()
    tmovies = TopTenMovies.objects.all()
    season = Season.objects.all()
    
    # Encoding movie image and video to base64
    for movie in movies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in hmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in tmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in season:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    return render(request, 'netflix/home_basic.html', {'movies': movies, 'hmovies': hmovies, 'tmovies':tmovies,'season':season})

def home_standard(request):
    movies = AppMovie.objects.all()
    hmovies = HorrorMovies.objects.all()
    tmovies = TopTenMovies.objects.all()
    season = Season.objects.all()
    
    # Encoding movie image and video to base64
    for movie in movies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in hmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in tmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in season:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    return render(request, 'netflix/home_standard.html', {'movies': movies, 'hmovies': hmovies, 'tmovies':tmovies,'season':season})

def home_premium(request):
    movies = AppMovie.objects.all()
    hmovies = HorrorMovies.objects.all()
    tmovies = TopTenMovies.objects.all()
    season = Season.objects.all()
    
    # Encoding movie image and video to base64
    for movie in movies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in hmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in tmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in season:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    return render(request, 'netflix/home_premium.html', {'movies': movies, 'hmovies': hmovies, 'tmovies':tmovies,'season':season})


from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users
from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password_hash')

            try:
                # Query the user by email
                user = Users.objects.get(email=email)

                # Check the password
                if check_password(password, user.password_hash):
                    # Store user ID in session
                    request.session['user_id'] = user.user_id
                    request.session['selected_plan'] = user.subscription_plan  # Store the selected plan in session

                    messages.success(request, "You are now logged in!")

                    # Redirect to the correct home page based on the plan
                    if user.subscription_plan == 'Mobile':
                        return redirect('profile_mobile')
                    elif user.subscription_plan == 'Basic':
                        return redirect('profile_basic')
                    elif user.subscription_plan == 'Standard':
                        return redirect('profile_standard')
                    elif user.subscription_plan == 'Premium':
                        return redirect('profile_premium')
                    else:
                        return redirect('home')  # Default redirect if plan is not set

                else:
                    messages.error(request, "Invalid email or password.")
            except Users.DoesNotExist:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = LoginForm()

    return render(request, 'netflix/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render
from .models import MyMovieList,MyMovieList1

import base64

def my_list(request):
    my_list_entries = MyMovieList.objects.select_related('movie').all()
    my_list_entries1 = MyMovieList1.objects.select_related('movie').all()

    # Encode the video data in base64 and store it in a new attribute
    for entry in my_list_entries:
        if entry.movie.video_data:
            entry.video_data_b64 = base64.b64encode(entry.movie.video_data).decode('utf-8')

    for entry in my_list_entries1:
        if entry.movie.video_data:
            entry.video_data_b64 = base64.b64encode(entry.movie.video_data).decode('utf-8')

    return render(request, 'netflix/my_list.html', {
        'my_list_entries': my_list_entries, 
        'my_list_entries1': my_list_entries1
    })


from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import MyMovieList, AppMovie,MyMovieList1

from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import MyMovieList, AppMovie, MyMovieList1, HorrorMovies

def add_to_my_list(request, movie_id):
    movie = get_object_or_404(AppMovie, id=movie_id)
    my_list_entry, created = MyMovieList.objects.get_or_create(
        movie=movie,
        defaults={
            'video_data': request.POST.get('video_data', ''),
            'video_url': request.POST.get('video_url', ''),
            'added_at': timezone.now()
        }
    )
    
    if created:
        print(f"App Movie '{movie.title}' added to My List successfully.")
    else:
        print(f"App Movie '{movie.title}' is already in My List.")
    
    return redirect('my_list')


from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import HorrorMovies, MyMovieList1

def add_to_my_list_horror(request, movie_id):
    movie = get_object_or_404(HorrorMovies, id=movie_id)
    my_list_entry, created = MyMovieList1.objects.get_or_create(
        movie=movie,
        defaults={
            'video_data': request.POST.get('video_data', ''),
            'video_url': request.POST.get('video_url', ''),
            'added_at': timezone.now()
        }
    )

    if created:
        print(f"Horror movie '{movie.title}' added to My List successfully.")
    else:
        print(f"Horror movie '{movie.title}' is already in My List.")

    return redirect('my_list')

def home(request):
    movies = AppMovie.objects.all()
    hmovies = HorrorMovies.objects.all()
    tmovies = TopTenMovies.objects.all()
    season = Season.objects.all()
    
    # Encoding movie image and video to base64
    for movie in movies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in hmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in tmovies:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    for movie in season:
        if movie.image_data:
            movie.image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
        else:
            movie.image_base64 = None

        if movie.video_data:
            movie.video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
        else:
            movie.video_base64 = None

    return render(request, 'netflix/home.html', {'movies': movies, 'hmovies': hmovies, 'tmovies':tmovies,'season':season})

import base64
from django.shortcuts import get_object_or_404, render
from .models import AppMovie

def movie_click(request, movie_id):
    movie = get_object_or_404(AppMovie, id=movie_id)

    # Encoding movie image and video to base64
    image_base64 = None
    if movie.image_data:
        image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
    
    video_base64 = None
    if movie.video_data:
        video_base64 = base64.b64encode(movie.video_data).decode('utf-8')

    related_movies = AppMovie.objects.exclude(id=movie_id)[:8]  # Fetch related movies (you can customize this logic)
    
    return render(request, 'netflix/movie_click.html', {
        'movie': movie,
        'related_movies': related_movies,
        'image_base64': image_base64,
        'video_base64': video_base64
    })
def movie_click_horror(request, movie_id):
    movie = get_object_or_404(HorrorMovies, id=movie_id)

    # Encoding movie image and video to base64
    image_base64 = None
    if movie.image_data:
        image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
    
    video_base64 = None
    if movie.video_data:
        video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
    
    return render(request, 'netflix/movie_click_horror.html', {
        'movie': movie,
        'image_base64': image_base64,
        'video_base64': video_base64
    })

def movie_click_top_ten(request, movie_id):
    movie = get_object_or_404(TopTenMovies, id=movie_id)

    # Encoding movie image and video to base64
    image_base64 = None
    if movie.image_data:
        image_base64 = base64.b64encode(movie.image_data).decode('utf-8')
    
    video_base64 = None
    if movie.video_data:
        video_base64 = base64.b64encode(movie.video_data).decode('utf-8')
    
    return render(request, 'netflix/movie_click_top_ten.html', {
        'movie': movie,
        'image_base64': image_base64,
        'video_base64': video_base64
    })
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import base64
from .models import Season, Episode

def season_click(request, season_id):
    # Fetch the specific season
    season = get_object_or_404(Season, id=season_id)

    # Encode image and video data for the season
    image_base64 = base64.b64encode(season.image_data).decode('utf-8') if season.image_data else None
    video_base64 = base64.b64encode(season.video_data).decode('utf-8') if season.video_data else None

    # Fetch and encode all episodes of the season
    episodes = season.episodes.all()
    encoded_episodes = []
    for episode in episodes:
        episode_video_base64 = None
        if episode.video_data:
            try:
                episode_video_base64 = base64.b64encode(episode.video_data).decode('utf-8')
            except Exception as e:
                print(f"Error encoding video for episode {episode.title}: {e}")

        encoded_episodes.append({
            'id': episode.id,
            'title': episode.title,
            'description': episode.description,
            'duration': episode.duration,
            'release_date': episode.release_date,
            'video_base64': episode_video_base64,  # Store base64 encoded video
        })

    # Get the redirect_url parameter from the request, default to home
    redirect_url = request.GET.get('redirect_url', reverse('home'))

    context = {
        'season': season,
        'image_base64': image_base64,
        'video_base64': video_base64,
        'episodes': encoded_episodes,
        'redirect_url': redirect_url,  # Add redirect_url to the context
    }

    return render(request, 'netflix/season_click.html', context)
def episode_play(request, season_id, episode_id):
    season = Season.objects.get(id=season_id)
    episode = Episode.objects.get(id=episode_id)

    # Ensure video data exists
    video_base64 = None
    if episode.video_data:
        video_base64 = base64.b64encode(episode.video_data).decode('utf-8')  # Base64 encode the video data

    # Get the redirect_url parameter from the request, default to home
    redirect_url = request.GET.get('redirect_url', reverse('home'))  # Default to 'home'

    context = {
        'season': season,
        'episode': episode,
        'video_base64': video_base64,
        'episodes': season.episodes.all(),  # Assuming you want to display other episodes in the same season
        'redirect_url': redirect_url,  # Add redirect_url to the context
    }

    return render(request, 'netflix/episode_play.html', context)






def popular(request):
    return render(request, 'netflix/popular.html')

from django.shortcuts import render
from .models import Users
from django.contrib.auth.decorators import login_required

def manage_profile(request):
    user_id = request.session.get('user_id')  # Get user ID from session

    if not user_id:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('/login/')  # Redirect to login if no user is logged in

    try:
        # Fetch user data
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('/home/')  # Redirect to home if user doesn't exist

    # Fetch all languages (if needed in the profile page)
    languages = Languages.objects.all()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user details
            messages.success(request, "Profile updated successfully!")
            return redirect('manage_profile')  # Redirect to the same page after successful update
        else:
            messages.error(request, "Failed to update profile. Please try again.")
    else:
        form = ProfileForm(instance=user)

    return render(request, 'netflix/manage_profile.html', {
        'form': form,
        'user': user,
        'languages': languages
    })

def edit_profile(request):
    user = request.user  # Get the currently logged-in user
    Language = Languages.objects.all()
    data = Users.objects.filter(user_id=user.id).first()  # Fetch the user's data

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=data)
        if form.is_valid():
            form.save()  # Save the updated user data to the database
            return redirect('manage_profile')  # Redirect to the profile page
    else:
        form = ProfileForm(instance=data)

    return render(request, 'netflix/edit_profile.html', {'form': form,'language':Language})

def transfer_profile(request):
    return render(request, 'netflix/transfer_profile.html')

def accounts(request):
    return render(request, 'netflix/accounts.html')

# Fetch movie details dynamically
def movie_detail(request, movie_id):
    # Try fetching the movie from either AppMovie or HorrorMovies
    try:
        movie = get_object_or_404(AppMovie, id=movie_id)
        movie_type = 'app_movie'  # Identifying movie type
    except AppMovie.DoesNotExist:
        movie = get_object_or_404(HorrorMovies, id=movie_id)
        movie_type = 'horror_movie'  # Identifying movie type

    image_base64 = None
    video_base64 = None

    # Check if the movie has an image and decode it to base64
    if movie.image_data:
        image_base64 = f"data:image/jpeg;base64,{base64.b64encode(movie.image_data).decode('utf-8')}"
    else:
        image_base64 = "data:image/jpeg;base64,DEFAULT_IMAGE_BASE64_STRING"  # Replace with actual base64 string for default image

    # Check if the movie has a video and decode it to base64
    if movie.video_data:
        video_base64 = f"data:video/mp4;base64,{base64.b64encode(movie.video_data).decode('utf-8')}"
    else:
        video_base64 = None  # Or placeholder string for no video

    # Pass the movie data to the template
    return render(request, 'netflix/movie_click.html', {
        'movie': movie,
        'image_base64': image_base64,
        'video_base64': video_base64,
    })


from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def upload_horror(request):
    if request.method == "POST":
        form = HorrorForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image_data = request.FILES['image_data'].read()
            instance.video_data = request.FILES['video_data'].read()
            instance.save()
            return redirect('home')
        else:
            logger.error("Form is not valid: %s", form.errors)
            return HttpResponse("Form is invalid!", status=400)
    else:
        form = HorrorForm()
    return render(request, 'netflix/upload_horror.html', {'form': form})

def upload_season(request):
    if request.method == "POST":
        form = SeasonForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image_data = request.FILES['image_data'].read()
            instance.video_data = request.FILES['video_data'].read()
            instance.save()
            return redirect('home')
        else:
            logger.error("Form is not valid: %s", form.errors)
            return HttpResponse("Form is invalid!", status=400)
    else:
        form = SeasonForm()
    return render(request, 'netflix/upload_season.html', {'form': form})

def upload_data(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image_data = request.FILES['image_data'].read()
            instance.video_data = request.FILES['video_data'].read()
            instance.save()
            return redirect('home')
        else:
            logger.error("Form is not valid: %s", form.errors)
            return HttpResponse("Form is invalid!", status=400)
    else:
        form = MovieForm()
    return render(request, 'netflix/upload_data.html', {'form': form})

def upload_top_ten(request):
    if request.method == "POST":
        form = top_ten(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image_data = request.FILES['image_data'].read()
            instance.video_data = request.FILES['video_data'].read()
            instance.save()
            return redirect('home')
        else:
            logger.error("Form is not valid: %s", form.errors)
            return HttpResponse("Form is invalid!", status=400)
    else:
        form = top_ten()
    return render(request, 'netflix/upload_top_ten.html', {'form': form})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EpisodeForm
import logging

logger = logging.getLogger(__name__)

def upload_episode(request):
    if request.method == "POST":
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            
            # Handle the video and image data
            if 'video_data' in request.FILES:
                instance.video_data = request.FILES['video_data'].read()  # Reading the video file as binary data

            # Handle other fields, such as image if applicable (add image_data if you want it)
            # if 'image_data' in request.FILES:
            #     instance.image_data = request.FILES['image_data'].read()

            instance.save()  # Save the episode to the database
            return redirect('home')  # Redirect to a success page
        else:
            logger.error("Form is not valid: %s", form.errors)
            return HttpResponse("Form is invalid!", status=400)
    else:
        form = EpisodeForm()

    return render(request, 'netflix/upload_episode.html', {'form': form})
