from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(AuthenticationForm):
	remember = forms.BooleanField(required=False, initial=True)

class UserNewForm(UserCreationForm):
	email = forms.EmailField(required=False, label='Email (for notifications only)')

	def clean_email(self):
	    email = self.cleaned_data['email']
	    if email and User.objects.filter(email=email).exists():
	        raise forms.ValidationError("This email address is already in use")
	    return email

class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
    
	def clean_email(self):
	    email = self.cleaned_data['email']
	    username = self.instance.username
	    if email and User.objects.filter(email=email).exclude(username=username).exists():
	        raise forms.ValidationError("This email address is already in use")
	    return email
