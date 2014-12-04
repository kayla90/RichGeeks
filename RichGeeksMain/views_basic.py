from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from github import Github
# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

from django.db.models import Q
from django.db import transaction

# Used to send mail from within Django
from django.core.mail import send_mail

from mimetypes import guess_type
from django.core import serializers

from RichGeeksMain.models import *
from RichGeeksMain.forms import *

import json
import requests

GITHUB_PARAM = {'client_id': '9cb96333069fb96e1196',
	'client_secret': '425a2b4cf5f0b142a342db25fa642bf32b04c1b8'}

def index(request):
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	registerform = RegisterForm()
	signinform = SigninForm()
	return render(request, 'index.html', {
		'registerform': registerform,
		'signinform'  : signinform})

def get_github_token(code):
	params = GITHUB_PARAM
	params['code'] = code
	headers = {'Accept': 'application/json'}
	r = requests.post("https://github.com/login/oauth/access_token", params=params
				, headers=headers)
	if 'access_token' in r.json():
		return r.json()['access_token']
	else:
		return None

def get_github_login(oauth_token):
	headers = {'Authorization': 'token ' + oauth_token}
	r = requests.get('https://api.github.com/user', headers=headers)
	if 'login' in r.json():
		return r.json()['login']
	else:
		return None

@transaction.atomic
def register(request):
	context = {}
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	context['signinform'] = SigninForm()
	# Just display the login page if this is a GET request
	if request.method == 'GET':
		context['registerform'] = RegisterForm()
		context['register'] = True

		if 'code' in request.GET:
			oauth_token = get_github_token(request.GET['code'])
			if oauth_token:
				github_login = get_github_login(oauth_token)
				context['github'] = github_login
				context['registerform'].fields["username"].initial = github_login
				context['registerform'].fields["github_token"].initial = oauth_token


			params = GITHUB_PARAM
			params['code'] = request.GET['code']
			headers = {'Accept': 'application/json'}
			r = requests.post("https://github.com/login/oauth/access_token", params=params
				, headers=headers)
			if 'access_token' in r.json():
				oauth_token = r.json()['access_token']
				headers = {'Authorization': 'token ' + oauth_token}
				r = requests.get('https://api.github.com/user', headers=headers)
				github_login = r.json()['login']
				context['registerform'].fields["username"].initial = github_login
				context['registerform'].fields["github_login"].initial = github_login
				context['github'] = github_login
		
		return render(request, 'index.html', context)

	registerform = RegisterForm(request.POST)
	context['registerform'] = registerform

	if not registerform.is_valid():
		context['register'] = True
		return render(request, 'index.html', context)

    # Creates the new user from the valid form data
	new_user = User.objects.create_user(
    	username=registerform.cleaned_data['username'], \
    	email=registerform.cleaned_data['email'],\
    	password=registerform.cleaned_data['password1']
    	)

	new_user.is_active = False
	new_user.save()

	new_profile = UserProfile(user=new_user)
	language = 'Python'
	if 'github_token' in request.POST and request.POST['github_token']:
		github_login = get_github_login(request.POST['github_token'])
		new_profile.github_login = github_login
		USER = github_login
		ACCESS_TOKEN = '8e87a4670383b27a163b8a020955b4761a6da3dc'
		client = Github(ACCESS_TOKEN, per_page=100)
		user = client.get_user(USER)
	 	repos = user.get_repos()
	 	candidate_language = {}
		for r in repos:
			languages = r.get_languages()
			for key in languages:
				if key in candidate_language:
					candidate_language[key] = candidate_language[key] + languages[key]
				else:
					candidate_language[key] = languages[key]
		if len(candidate_language) > 0:
			sorted(candidate_language, key=candidate_language.get, reverse=True)
			key, value = candidate_language.popitem()
			language = key
	new_profile.save()
	#link language information - github_login is username
    
	git_profile = GitHubProfile(githuber = new_profile, language = language)
	git_profile.save()

	token = default_token_generator.make_token(new_user)
	email_body = """
Welcome to Rich Geeks.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
		reverse('confirm', args=(new_user.id, token)))

	send_mail(subject="Verify your email address",
              message= email_body,
              from_email="admin@richgeeks.com",
              recipient_list=[new_user.username])

	context['email'] = registerform.cleaned_data['email']
	return render(request, 'needs-confirmation.html', context)

def signin(request):
	context = {}
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	context['registerform'] = RegisterForm()
	# Just display the login page if this is a GET request
	if request.method == 'GET':
		context['signinform'] = SigninForm()
		context['signin'] = True
		return render(request, 'index.html', context)

	signinform = SigninForm(request.POST)
	context['signinform'] = signinform

	if not signinform.is_valid():
		context['signin'] = True
		return render(request, 'index.html', context)

	user = authenticate(username=signinform.cleaned_data['username'],
						password=signinform.cleaned_data['password'])
	# if the user doesn't check remember me, set expiry to 0
	if not signinform.cleaned_data['remember_me']:
		request.session.set_expiry(0)

	login(request, user)
	return redirect(reverse('home'))

@transaction.atomic
def confirm_registration(request, id, token):
    user = get_object_or_404(User, id=id)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
    	print('No')
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})

@login_required
def get_profile_image(request, id):
    profile = get_object_or_404(UserProfile, user=id)
    if not profile.profile_image:
        raise Http404

    content_type = guess_type(profile.profile_image.name)
    return HttpResponse(profile.profile_image, content_type=content_type)

@login_required
def profile(request, userid):
	context = {}
	# if the user doesn't exist, return to the home page
	if not len(User.objects.filter(id = userid)) > 0:
		return redirect(reverse('home'))

	profile_user = User.objects.get(id = userid)
	profile = UserProfile.objects.get(user = userid)
	context['profile_user'] = profile_user
	context['profile'] = profile

	# check if are friends
	if request.user.id != userid:
		if User.objects.get(id = userid) in profile.friends.all():
			context['friend'] = True
	
	return render(request, "profile.html", context)

@login_required
def profile_overview(request, userid):
	profile = get_object_or_404(UserProfile, user=userid)
	return HttpResponse(render_to_string('profile-overview.html', { 'profile': profile }))

@login_required
def profile_analysis(request, userid):
	profile = get_object_or_404(UserProfile, user=userid)
	return HttpResponse(render_to_string('analysis.html', { 'profile': profile }))


@login_required
def edit(request):
	context = {}

	userprofileform = UserProfileForm(
			instance=UserProfile.objects.get(user=request.user))
	context['passwordform'] = PasswordForm(request.user)

	if request.method == 'GET':
		context['userprofileform'] = userprofileform
		return render(request, 'edit.html', context)

	userprofileform = UserProfileForm(request.POST, request.FILES,
		instance=UserProfile.objects.get(user=request.user.id))

	if not userprofileform.is_valid():
		context['userprofileform'] = userprofileform
		return render(request, 'edit.html', context)

	userprofileform.save()
	return redirect(reverse('profile', args=(request.user.id,)))

@login_required
@transaction.atomic
def change_password(request):
	context = {}
	if request.method == 'GET':
		return redirect(reverse('edit'))

	passwordform = PasswordForm(request.user, request.POST)
	if not passwordform.is_valid():
		for error in passwordform.errors.values():
			messages.add_message(request, messages.INFO, error)
		return redirect(reverse('edit'))

	user = request.user
	user.set_password(passwordform.cleaned_data['password1'])
	user.save()
	messages.add_message(request, messages.INFO, "Password changed successfully.")

	return redirect(reverse('profile', args=(request.user.id,)))

def forget_password(request):
	if request.method == 'GET':
		emailform = EmailForm()
		return render(request, 'forget-password.html', {'form': emailform})
	emailform = EmailForm(request.POST)
	if not emailform.is_valid():
		return render(request, 'forget-password.html', {'form': emailform})

	email = emailform.cleaned_data['email']
	user=User.objects.get(email__exact=email)

	token = default_token_generator.make_token(user)
	email_body = """
Please click the link below to verify your email address
and continue to change the password of your account:

  http://%s%s
""" % (request.get_host(), 
		reverse('reset_password', args=(user.id, token)))

	send_mail(subject="Change your password - Rich Geeks",
              message= email_body,
              from_email="admin@richgeeks.com",
              recipient_list=[user.email])


	return render(request, 'forget-password.html', {'email': email})

def reset_password(request, id, token):
	user = get_object_or_404(User, id=id)

	# Send 404 error if token is invalid
	if not default_token_generator.check_token(user, token):
		print('No')
		raise Http404

	if request.method == 'GET':
		form = ForgetPasswordForm()
		return render(request, 'change-password.html', { 'form': form, 'id': id, 'token': token })

	form = ForgetPasswordForm(request.POST)
	if not form.is_valid():
		return render(request, 'change-password.html', { 'form': form, 'id': id, 'token': token })

	user = User.objects.get(id__exact=id)
	user.set_password(form.cleaned_data['password1'])
	user.save()

	return redirect(reverse('login'))
