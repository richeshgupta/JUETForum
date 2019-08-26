from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class question(models.Model):
	author_q = models.ForeignKey(User, on_delete=models.CASCADE,)
	title_q = models.CharField(max_length=50,verbose_name='Title of Question')
	notice_q = models.TextField(max_length=1000,default='',verbose_name="Description of Question")
	date_q = models.DateTimeField(default = timezone.now,verbose_name="Date/Time")
	url_q = models.URLField(max_length=100,blank = True,verbose_name="URL reference")
	tag1_q = models.CharField(max_length=15,verbose_name="Tag 1")
	tag2_q = models.CharField(max_length=15,verbose_name="Tag 2")
	views = models.PositiveIntegerField(default = 0)
	def __str__(self):
		return self.title_q
	
	def get_absolute_url(self):
		return reverse('forum-home')

	def rep(self):
		return self.author_q

class answer(models.Model):
	title_a = models.CharField(max_length=50,verbose_name='Title of Answer')
	author_a = models.ForeignKey(User, on_delete=models.CASCADE,)
	notice_a = models.TextField(max_length=2200,default="",verbose_name='Describe Answer')
	date_a = models.DateTimeField(default = timezone.now,verbose_name='Date/Time')
	url_a = models.URLField(max_length=100,blank = True,verbose_name='URL reference')
	ques = models.ForeignKey(question,on_delete=models.CASCADE,verbose_name='Select Question')
	upvotes = models.IntegerField(default = 0)
	downvoted_by = models.ManyToManyField(User,related_name='downvoters')
	upvoted_by = models.ManyToManyField(User,related_name='upvoters')
	views = models.PositiveIntegerField(default=0)
	def __str__(self):
		return self.notice_a
	
	def get_absolute_url(self):
		return reverse('forum-home')

class reportques(models.Model):
	reported_q = models.ForeignKey(question,on_delete=models.CASCADE)
	reported_by  = models.ForeignKey(User,on_delete = models.CASCADE)

class reportans(models.Model):
	reported_a = models.ForeignKey(answer,on_delete=models.CASCADE)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	#image = models.ImageField(default='default.jpg', upload_to='profie/pics')

	def __str__(self):
		return f'{self.user.username} Profile' 

class msgs(models.Model):
	sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Sender")
	receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
	date = models.DateTimeField(default = timezone.now)
	text = models.TextField(max_length=100,default=" ",verbose_name='Message')

