from django.shortcuts import  render , redirect
from .forms import register_form_auth
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def home_page_request (request):
	return render (request=request, template_name="main/home.html")

def register_request(request):

	if request.method == "POST": # check request
		form_login = register_form_auth(request.POST)
		if form_login.is_valid(): # if valid
			user = form_login.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, "register %s ok." % (form_login.cleaned_data.get('username')))
			return redirect('/')
		else: # if faild
			messages.error(request, "Unsuccessful registration. Invalid information.")
			return redirect('/register_error')
	else: # if reguest login page
		return render (request=request, template_name="main/register.html")

def login_request(request):

	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				messages.info(request, f'You are now logged in as %s' % request.POST['username'])
				return redirect('/')

			else:
				return redirect('/login_error')

		else:
			return redirect('/login_error')

	else:
		return render(request=request, template_name="main/testsinup.html")

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('/login')

def register_error(request):
	return render (request=request, template_name="main/register_error.html")

def login_error(request):
	return render (request=request, template_name="main/login_error.html")
