from django import forms

from django.contrib.auth.models import User
from models import *

from datetime import date
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
	username  = forms.CharField(max_length = 30,
								widget = forms.TextInput(attrs={
									'class': 'form-control',
									'placeholder': 'Username',
									'required': 'true'}))
	email     = forms.CharField(max_length = 200,
								widget = forms.EmailInput(attrs={
									'class': 'form-control',
									'placeholder': 'Email address',
									'required': 'true'}))

	password1 = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control',
                                	'placeholder': 'Password',
                                	'required': 'true'}))
	password2 = forms.CharField(max_length = 200,  
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control',
                                	'placeholder': 'Password confirm',
                                	'required': 'true'}))
	github_token = forms.CharField(max_length = 200,
								widget = forms.HiddenInput(),
								required=False)

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		# Generally return the cleaned data we got from our parent.
		return cleaned_data

	def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
		return username

	def clean_email(self):
        # Confirms that the email is not already present in the
        # User model database.
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__exact=email):
			raise forms.ValidationError("Email is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
		return email

class SigninForm(forms.Form):
	username    = forms.CharField(max_length = 30,
								widget = forms.TextInput(attrs={
									'class': 'form-control',
									'placeholder': 'Username',
									'required': 'true'}))
	password    = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control',
                                	'placeholder': 'Password',
                                	'required': 'true'}))
	remember_me = forms.BooleanField(required=False)
	
	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("Cannot validate the email-password pair.")
		elif not user.is_active:
			raise forms.ValidationError("The user is not active. Please click the link in your email.")
           
		return self.cleaned_data

class SendMessageForm(forms.Form):
	message_content = forms.CharField(max_length=10000)
	receiver_userid = forms.CharField(max_length=100)

	def clean(self):
		cleaned_data = super(SendMessageForm, self).clean()

	def clean_receiver_userid(self):
		receiver_userid = self.cleaned_data.get('receiver_userid')
		if not User.objects.filter(id=receiver_userid):
			raise form.ValidationError("Receiver does not exist")
		return receiver_userid


class ReplyMessageForm(forms.Form):
	message_content = forms.CharField(max_length=10000)
	ancestor_message_id = forms.IntegerField()

	def clean(self):
		cleaned_data = super(ReplyMessageForm, self).clean()

	def clean_ancestor_message_id(self):
		ancestor_message_id = self.cleaned_data.get('ancestor_message_id')
		if not Message.objects.filter(id=ancestor_message_id):
			raise form.ValidationError("Ancestor not correct")	
		return ancestor_message_id


class FeedbackProjectForm(forms.Form):
	feedback_rating = forms.IntegerField()
	feedback_text = forms.CharField(max_length=10000)

	def clean(self):
		cleaned_data = super(FeedbackProjectForm, self).clean()

	def clean_feedback_rating(self):
		feedback_rating = self.cleaned_data.get('feedback_rating')
		if not (1 <= feedback_rating <= 5):
			raise form.ValidationError("feedback rating not correct")	
		return feedback_rating


class EvaluationProjectForm(forms.Form):
	evaluation_rating = forms.IntegerField()
	evaluation_text = forms.CharField(max_length=10000)

	def clean(self):
		cleaned_data = super(EvaluationProjectForm, self).clean()

	def clean_evaluation_rating(self):
		evaluation_rating = self.cleaned_data.get('evaluation_rating')
		if not (1 <= evaluation_rating <=5):
			raise form.ValidationError("Evaluation rating not correct")
		return evaluation_rating


class ApplyProjectForm(forms.Form):
	description_experience = forms.CharField(max_length=10000)
	proposal_file = forms.FileField(required=False,
			widget=forms.FileInput)
	expected_earning = forms.IntegerField()
	expected_time = forms.IntegerField()

	def clean(self):
		cleaned_data = super(ApplyProjectForm, self). clean()


class PostProjectForm(forms.Form):
	title = forms.CharField(max_length=100)
	description = forms.CharField(max_length=100000)
	budget = forms.IntegerField()
	workload = forms.IntegerField()
	date_start = forms.DateField()
	languages = forms.MultipleChoiceField(required=False,
			widget=forms.CheckboxSelectMultiple, 
			choices=LANGUAGE_CHOICES)
	description_file = forms.FileField(required=False,
			widget=forms.FileInput)

	def clean(self):
		cleaned_data = super(PostProjectForm, self).clean()

class UserProfileForm(forms.ModelForm):
	class Meta:
		model   = UserProfile
		exclude = ['user', 'rand_string','friends']
		widgets = {
			"full_name":forms.TextInput(attrs={'class':'form-control'}),
			"profile_image":forms.ClearableFileInput(),
			"birthday":forms.DateInput(attrs={'type':'date','class':'form-control'}),
			"address":forms.TextInput(attrs={'class':'form-control'}),
			"country":forms.TextInput(attrs={'class':'form-control'}),
			"city":forms.TextInput(attrs={'class':'form-control'}),
			"phone":forms.TextInput(attrs={'class':'form-control'}),
                  }

class PasswordForm(forms.Form):
	current = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control'}))
	password1 = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control'}))
	password2 = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control'}))

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(PasswordForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(PasswordForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data

	def clean_current(self):
		current = self.cleaned_data.get('current')
		user = authenticate(username=self.user.username, password=current)
		if user is None:
			raise forms.ValidationError("Wrong password.")

		# Generally return the cleaned data we got from our parent.
		return current

class EmailForm(forms.Form):
	email = forms.EmailField(
							widget = forms.EmailInput(attrs={
                                	'class': 'form-control',
                                	'placeholder': 'Email address',
                                	'required': 'true'})
							)
	def clean_email(self):
		email = self.cleaned_data.get('email')
		user = User.objects.filter(email__exact=email)
		if not user:
			raise forms.ValidationError("User does not exist.")

		return email

class ForgetPasswordForm(forms.Form):
	password1 = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control',
                                	'placeholder': 'Password',
                                	'required': 'true'}))
	password2 = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={
                                	'class': 'form-control',
                                	'placeholder': 'Reenter password',
                                	'required': 'true'}))

	def clean(self):
		cleaned_data = super(ForgetPasswordForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data

class PostNewsFeedForm(forms.Form):
	news_feed_text = forms.CharField(max_length=1000)
	image = forms.ImageField(widget=forms.FileInput(), required=False)

	def clean(self):
		print("gothere")
		cleaned_data = super(PostNewsFeedForm, self).clean()