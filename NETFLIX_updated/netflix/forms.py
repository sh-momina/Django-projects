# forms.py
from django import forms
from .models import Users,AppMovie,Languages,HorrorMovies,Complaint,Faq,TopTenMovies

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(),
        }
    class Meta:
        model = Users
        fields = ['email', 'password_hash','full_name']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description']

class top_ten(forms.ModelForm):
    class Meta:
        model = TopTenMovies
        fields = ['title', 'description', 'duration', 'genre', 'rating','release_year']

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password_hash = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields = ['language_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'full_name','language']  # Allow editing only email and full name
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class MovieForm(forms.ModelForm):
    class Meta:
        model = AppMovie
        fields = ['title', 'description', 'duration', 'genre', 'rating','release_year']


class HorrorForm(forms.ModelForm):
    class Meta:
        model = HorrorMovies
        fields = ['title', 'description', 'duration', 'genre', 'rating','release_year']

from django import forms
from .models import Season, Episode

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['title', 'description', 'release_year', 'genre', 'season_number']


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['season', 'title', 'description', 'duration', 'rating']
