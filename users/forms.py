from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class kk(UserCreationForm):
	YEAR = ((1,"First",),(2,"Second"),(3,"Third"),(4,"Fourth"))
	email = forms.EmailField(max_length=60)
	first_name = forms.CharField(max_length = 20)
	last_name = forms.CharField(max_length=20)
	Year = forms.ChoiceField(choices = YEAR)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','Year','email','password1','password2']
