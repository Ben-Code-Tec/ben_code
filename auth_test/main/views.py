from django.shortcuts import  render , redirect
from .forms import register_form_auth
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import requests as RQ
import re
# from github import Github

def home_page_request (request):
	return render (request=request, template_name="main/home.html")

def register_request(request , context={}):

	try:
		if request.GET['code'] != None:
			context = github_auth(request , return_def = 'context')

	except:
		pass

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
		return render (request=request, template_name="main/sign up.html" , context=context)

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
		return render(request=request, template_name="main/sign in.html")

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('/login')

def register_error(request):
	return render (request=request, template_name="main/register_error.html")

def error_auth(request):
	return render (request=request, template_name="main/Error_auth.html")

def login_error(request):
	return render (request=request, template_name="main/login_error.html")

def test_html(request):
	return render (request=request, template_name="main/test.html")

def github_auth(request , return_def='all'):

	client_id = '908f44f68a29c7b594db'
	client_secret = 'ad49e5c27a8a481b9619307c377e3701801baabe'
	code = request.GET['code']
	github_respond = RQ.post('https://github.com/login/oauth/access_token?code=%s&client_secret=%s&client_id=%s' % (code , client_secret , client_id))
	# print (github_respond.text)
	access_token = re.findall(r'token\=([a-zA-Z1-90\_]+)', github_respond.text)[0]

	g = Github(access_token)
	user_g = g.get_user()
	name_github = user_g.name
	if name_github == None:
		name_github = user_g.login
	for har_email in user_g.get_emails():
		valid_email = re.findall(r'@gmail.com', har_email[0])
		if valid_email != []:
			email_github = har_email[0]
			break

	my_dict = {'name_github':name_github , 'email_github':email_github}

	if return_def == 'context':
		return my_dict

	else:
		return redirect("/register?context={'name_github':%s , 'email_github':%s}" % (name_github , email_github))
