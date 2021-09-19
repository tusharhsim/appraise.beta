from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Person, RequestService, ProvideService, JobAlert, HiringAlert

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text=None)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, help_text=None)

    class Meta:
        model = User
        fields = ['username']
        help_texts = {k:"" for k in fields}

class PersonUpdateForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ['pin_code', 'name', 'contact', 'dob', 'gender', 'visibility']

class RequestServiceForm(forms.ModelForm):
	class Meta:
		model = RequestService
		fields = ['title', 'tag', 'contact', 'deadline', 'location', 'pay_scale']

class ProvideServiceForm(forms.ModelForm):
	class Meta:
		model = ProvideService
		fields = ['title', 'tag', 'contact', 'location', 'pay_scale']

class ApplyForJob(forms.ModelForm):
	class Meta:
		model = JobAlert
		fields = ['pin_code', 'contact', 'ask_amount']

class HireFreelancer(forms.ModelForm):
	class Meta:
		model = HiringAlert
		fields = ['pin_code', 'contact', 'bid_amount']