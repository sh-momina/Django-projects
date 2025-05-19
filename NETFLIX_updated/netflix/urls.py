# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('signup/', views.signup, name='signup'),
    path('save_subscription/', views.save_subscription_and_payment, name='save_subscription_and_payment'),
    path('signup3/', views.signup3, name='signup3'),  
    path('subscribed/', views.subscribed, name='subscribed'), 
    path('signup_step2/', views.signup_step2, name='signup_step2'), 
    path('profile_mobile/', views.profile_mobile, name='profile_mobile'),
    path('profile_basic/', views.profile_basic, name='profile_basic'),
    path('profile_standard/', views.profile_standard, name='profile_standard'),
    path('profile_premium/', views.profile_premium, name='profile_premium'),
    path('home_mobile/', views.home_mobile, name='home_mobile'),
    path('home_basic/', views.home_basic, name='home_basic'),
    path('home_standard/', views.home_standard, name='home_standard'),
    path('home_premium/', views.home_premium, name='home_premium'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('movie_click/<int:movie_id>/', views.movie_click, name='movie_click'),
    path('movie_click_horror/<int:movie_id>/', views.movie_click_horror, name='movie_click_horror'),
    path('movie_click_top_ten/<int:movie_id>/', views.movie_click_top_ten, name='movie_click_top_ten'),
    path('popular/', views.popular, name='popular'),
    path('manage_profile/', views.manage_profile, name='manage_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('transfer_proflie/', views.transfer_profile, name='transfer_profile'),
    path('accounts/', views.accounts, name='accounts'),
    path('upload_data/', views.upload_data, name='upload_data'),
    path('upload_horror/', views.upload_horror, name='upload_horror'),
    path('upload_season/', views.upload_season, name='upload_season'),
    path('upload_episode/', views.upload_episode, name='upload_episode'),
    path('top_ten/', views.upload_top_ten, name='top_ten'),
    path('my-list/', views.my_list, name='my_list'),
    path('add-to-my-list/<int:movie_id>/', views.add_to_my_list, name='add_to_my_list_appmovie'),
    path('add-to-my-list/horror/<int:movie_id>/', views.add_to_my_list_horror, name='add_to_my_list_horror'),
    path('help/', views.help_page, name='help_page'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('season_click/<int:season_id>/', views.season_click, name='season_click'),
    path('season/<int:season_id>/episode/<int:episode_id>/', views.episode_play, name='episode_play'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
