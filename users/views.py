from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import  authenticate
from .forms import kk as SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.views import PasswordChangeDoneView,PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# from django.contrib.auth

# from .forms import kk

def not_logged_in(request):
	return render(request,'users/not_logged_in.html',{})

def menu(request):
	return render(request,'users/initial.html',{})
	
def about(request):
	return render(request,'users/about.html',{})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'AskJUET - Verify'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request,'users/success-confirm.html',{})
    else:
        form = SignupForm()
    return render(request,'users/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
       uid = force_text(urlsafe_base64_decode(uidb64))
       user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
       user = None
    if user is not None and account_activation_token.check_token(user, token):
       user.is_active = True
       user.save()
       login(request, user)
        # return redirect('home')
       return render(request,"users/success.html",{})
    else:
       return render(request,"users/invalid-link.html",{})

def privacy(request):
  return render(request,"users/privacy.html",{})

class change_pass(PasswordChangeView,LoginRequiredMixin):
  template_name = "users/change_pass.html"
class change_pass_done(PasswordChangeDoneView,LoginRequiredMixin):
  template_name="users/change_pass_done.html"