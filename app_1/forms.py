from django import forms
from .models import contact,marks_sheet

class djangoform(forms.Form):
    name = forms.CharField(label="name", max_length=20, widget=forms.TextInput)
    num1 = forms.CharField(label= "number1", max_length=5, widget=forms.NumberInput)
    num2 = forms.CharField(label= "number2", max_length=5, widget=forms.NumberInput)

    # widgets -> type, textarea , time, numberinput, number boolean input etc..


class marksform(forms.ModelForm):
    class Meta:
        model = marks_sheet
        fields = ['name','marks']

class modelform(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['full_name', 'email', 'phone_number', 'message']

