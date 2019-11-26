from django.shortcuts import render,redirect
from .models import question,answer
from .forms import questionForm,answerForm,msgs_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins	import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import reportques,reportans,msgs
from django.contrib.auth.models import User

class index_forum(ListView): 
	model = question
	template_name = 'main/index.html'
	context_object_name = 'datas'
	ordering = ['-date_q']
	def count(request,pk):
		k = answer.objects.get(ques=pk).count
		return k 

class forum_detail(DetailView):
	model = question
	template_name= 'main/detailpost.html'
	ordering = ['-date_q']


class answer_independent(DetailView):
	model = answer
	template_name = 'main/ans.html'
	def get_context_object(self,**kwargs):
		self.views+=1;
		self.save()
		return super().get_context_object(**kwargs)

class PostCreate(LoginRequiredMixin,CreateView):
	model = question
	fields= ['title_q','notice_q','url_q','tag1_q','tag2_q',]
	context_object_name = 'form'
	template_name = 'main/forum_write.html'
	def form_valid(self,questionForm):
		questionForm.instance.author_q = self.request.user
		return super().form_valid(questionForm)

from .forms import answerForm
@login_required
def ans_create(request,pk):
	if request.method=='POST':
		form = answerForm(request.POST)
		if form.is_valid():
			form.instance.author_a = request.user
			form.instance.ques = question.objects.get(id = pk)
			form.save()
			form = answerForm()
			return render(request,"main/ans_write.html",{'form':form})
	else:
		form = answerForm()
		return render(request,"main/ans_write.html",{'form':form})



def answer_detail(request,pk):
	kquery = answer.objects.filter(ques = pk).order_by('-upvotes')
	context = {'kquery':kquery}
	return render(request,'main/detailanswer.html',context)

class question_delete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = question
	success_url = '/forum/'
	def test_func(self):
		test_case = self.get_object()
		if self.request.user == test_case.author_q:
			return True
		else:
			return False

class AnswerDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model  = answer
	success_url = '/forum/'
	def test_func(self):
		test_case = self.get_object()
		if self.request.user == test_case.author_a:
			return True
		else:
			return False

class QuestionUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = question
	fields= ['title_q','notice_q','date_q','url_q','tag1_q','tag2_q',]
	context_object_name = 'form'
	def form_valid(self,questionForm):
		questionForm.instance.author_q = self.request.user
		return super().form_valid(questionForm)
	def test_func(self):
		test_case = self.get_object()
		if self.request.user == test_case.author_q:
			return True
		else:
			return False

class AnswerUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = answer
	fields = ['notice_a','date_a','url_a',]
	context_object_name = 'form'
	def form_valid(self,answerForm):
		answerForm.instance.author_a = self.request.user
		return super().form_valid(answerForm)
	def test_func(self):
		test_case = self.get_object()
		if self.request.user == test_case.author_a:
			return True
		else:
			return False

@login_required
def upvotes(request,pk):
	query = answer.objects.get(id = pk)
	k = query.upvoted_by.all()
	k2 = query.downvoted_by.all()
	if request.user not in k:
		query.upvotes+=1;
		query.save();
		if request.user not in k2:
			query.upvoted_by.add(request.user)
			
		else:
			query.downvoted_by.remove(request.user)
		return render(request,"main/upvoted.html",{})
	else:
		return render(request,"main/already-upvoted.html",{})

@login_required
def downvotes(request,pk):
	query = answer.objects.get(id = pk)
	k = query.downvoted_by.all()
	k2 = query.upvoted_by.all()
	if request.user not in k:
		query.upvotes-=1;
		query.save();
		if request.user not in k2:
			query.downvoted_by.add(request.user)
		else:
			query.upvoted_by.remove(request.user)
		return render(request,"main/downvoted.html",{})
	else:
		return render(request,"main/already-downvoted.html",{})


@login_required
def reportq(request,pk):
	query = question.objects.get(id = pk)
	try:
		kquery = reportques.objects.get(reported_q=query,reported_by = request.user)
	except:
		kquery = reportques(reported_q = query,reported_by = request.user)
	kquery.save();
	return render(request,"main/reported.html",{})

@login_required
def reporta(request,pk):
	query = answer.objects.get(id = pk)
	try:
		kquery = reportans.objects.get(reported_a=query)
	except:
		kquery = reportans(reported_a = query)
	kquery.save();
	return render(request,"main/reported.html",{})

def profile(request,pk):
	qquery = question.objects.filter(author_q = pk)
	author = User.objects.get(id = pk)
	context= {'qquery':qquery,'author':author}
	return render(request,"main/profile.html",context)
def donate(request):
	return render(request,"main/donate.html",{})

def faqs(request):
	return render(request,"main/faqs.html",{})

def guidelines(request):
	return render(request,"main/guidelines.html",{})

def donors(request):
	return render(request,"main/donors.html",{})

class msgs_view(CreateView,LoginRequiredMixin):
	model = msgs
	fields = ["receiver","text"]
	context_object_name = "form"
	template_name = "main/send_msg.html"
	def form_valid(self,msgs_form):
		msgs_form.instance.sender = self.request.user
		return super().form_valid(msgs_form)
def forgot(request):
	return render(request,"main/forgot-pass.html",{})