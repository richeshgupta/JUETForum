from django import forms
from django.contrib.auth.models import User
from .models import question,answer,msgs
#from django.utils.translation import ugettext_lazy as _
class questionForm(forms.ModelForm):
	
	class Meta: 
		model = question
		fields= ['title_q','notice_q','url_q','tag1_q','tag2_q',]


class answerForm(forms.ModelForm):
	
	class Meta: 
		model = answer
		fields= ['title_a','ques','notice_a','url_a',]

class msgs_form(forms.ModelForm):
	class Meta:
		model = msgs
		fields = ['receiver','text']