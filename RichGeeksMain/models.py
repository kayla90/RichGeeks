from django.db import models
from django.contrib.auth.models import User

LANGUAGE_CHOICES = (
	('All', 'All'),
	('JavaScript', 'JavaScript'),
	('Ruby', 'Ruby'),
	('Java', 'Java'),
	('PHP', 'PHP'),
	('Python', 'Python'),
	('C++', 'C++'),
	('C', 'C'),
	('Objective-C', 'Objective-C'),
	('C#', 'C#'),
	('Shell', 'Shell'),
	('CSS', 'CSS'),
	('Perl', 'Perl'),
	)

CATEGORY_CHOICES = (
	("All", "All"),
	('Web Programming', 'Web Programming'),
	('Data Analysis', 'Data Analysis'),
	('Database Development', 'Database Development'),
	('Mobile Application', 'Mobile Application'),
	('Software Application', 'Software Application'),
	('System Administration', 'System Administration'),
	('Testing QA', 'Testing QA'),
	('Website Design', 'Website Design'),
	)

class UserProfile(models.Model):

	#extends the User, using a django OneToOneField
	#this contains the basic information of a User's firstname, 
	#	lastname, email, username, password, and is_active
	user = models.OneToOneField(User, primary_key=True)
	
	#This is a random string of chars, which is used for email confirmation
	#typically in the following two cases:
	#(1) after the registration of a user, activate the user account
	#(2) after the user forgot his password and asks for resetting the password
	rand_string = models.CharField(max_length=100, null=True, blank=True)
	
	full_name = models.CharField(max_length=100, null=True, blank=True)
	#User's list of friend, pointing to another "UserInfo" instance
	friends = models.ManyToManyField('self', through='Friend', symmetrical=False)

	#Basic Information: sex and birthday
	gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('F', 'Female')),blank=True)
	birthday = models.DateField(null=True, blank=True)

	#Contact Information: phone number and address
	phone = models.CharField(max_length=100, null=True, blank=True)
	country = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)

	#user's uploaded profile image
	profile_image = models.ImageField(upload_to="user_photo", default='user_photo/1.jpg')
	github_login = models.CharField(max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'user\'s profile: %s' % (self.user.username)


class Friend(models.Model):
	accepted = models.BooleanField(default=False)
	source = models.ForeignKey(UserProfile, related_name="friend_source")
	target = models.ForeignKey(UserProfile, related_name="friend_target")


#This is a model indicating a certain programming language and its length
#used in the following scenarios:
#(1)User's profile, indicating a user's proficiency in a certain language
#(2)Project info, the expected length of lines in a certain project
class Languages(models.Model):

	#languages of this item, this is a enum field
	#we can add more languages to this field if we want
	language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

	lines = models.IntegerField(default=0, blank=True, null=True)

	def __unicode__(self):
		return u'usage for language %s is %s' (self.language, self.lines)


#the data is retrieved mainly by two means:
#(1)Github Archive: http://www.githubarchive.org/, using Google BigQuery
#(2)Github Api: https://developer.github.com/v3
class GitHubProfile(models.Model):
	githuber = models.ForeignKey(UserProfile, related_name = "githuber")

	#languages used, this contains the list of languages that a user used in github repos
	language = models.CharField(max_length = 20)

	number_commits = models.IntegerField(default=0, blank=True)
	number_lines = models.IntegerField(default=0, blank=True)
	number_issues = models.IntegerField(default=0, blank=True)

	#there should be more information here
	#we'll dig in to that later

	def __unicode__(self):
		return u'github profile No.%s' (self.id)


class Message(models.Model):

	#sender and receiver of the message
	sender = models.ForeignKey(UserProfile, related_name="sender")
	receiver = models.ForeignKey(UserProfile, related_name="receiver")

	#the type of message, this determines the disply in the views
	message_type = models.CharField(max_length=20, choices=(
		('Apply Project', 'Apply Project'),
		('Friend Request', 'Friend Request'),
		('Assigned Project', 'Assigned Project'),
		))

	date = models.DateTimeField(auto_now_add=True)

	project = models.ForeignKey('Project', blank=True, null=True)
	project_application = models.ForeignKey('ProjectApplication', blank=True, null=True)

	#ancestor message, this is typically used in a reply chain
	#ancestor = models.ForeignKey('self', blank=True, null=True)

	#this is_active mark is to indicate whether a message has been deleted
	#In such case, we should not directy remove the instance from the database
	#instead, we should set this boolean field to false
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return u'message from %s to %s, with type: %s' (self.sender.user.username, self.receiver.user.username, self.message_type)


#Group of users, related to single or multiple projects
class ProjectGroup(models.Model):
	members = models.ManyToManyField(UserProfile)
	name = models.CharField(max_length=100, default="Group")
	

class Project(models.Model):

	owner = models.ForeignKey(UserProfile, related_name="owner")
	assignee = models.ForeignKey(UserProfile, null=True, blank=True, related_name="assignee")

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=100000)
	description_file = models.FileField(upload_to="project_file", blank=True, null=True)

	date_start 	= models.DateTimeField(blank=True, null=True) 
	date_create = models.DateTimeField(auto_now_add=True)
	date_closed = models.DateTimeField(blank=True, null=True)
	
	#expected language/skills of the project
	languages = models.ManyToManyField('Languages', blank=True, null=True)

	status = models.CharField(max_length=10, default='New', choices=(
		('New', 'New'),
		('Open', 'Open'),
		('Working', 'Working'),
		('Canceled', 'Canceled'),
		('Failed', 'Failed'),
		('Completed', 'Completed'),
		))

	budget = models.IntegerField()
	workload = models.IntegerField()

	applications = models.ManyToManyField('ProjectApplication', blank=True, null=True)

	#evaluation of the project, a score and a message
	#this evaluation comes from the project creator
	evaluated = models.BooleanField(default=False)
	evaluation_score = models.IntegerField(blank=True, null=True, choices=(
		(1, 'Awful'),
		(2, 'Not Satisfied'),
		(3, 'Fair'),
		(4, 'Good'),
		(5, 'Excellent'),
		))
	evaluation_text = models.CharField(max_length=10000, blank=True, null=True)
	
	#a list of feedback from other users, like comments
	feedback = models.ManyToManyField('ProjectFeedback')
	
	category = models.CharField(max_length=30, default="", choices=CATEGORY_CHOICES)
	

class ProjectFeedback(models.Model):
	feedback_rating = models.IntegerField(blank=True, null=True, choices=(
		(1, 'Awful'),
		(2, 'Not Satisfied'),
		(3, 'Fair'),
		(4, 'Good'),
		(5, 'Excellent'),
		))
	feedback_text = models.CharField(max_length=10000, blank=True, null=True)

class ProjectApplication(models.Model):
	user_profile = models.ForeignKey(UserProfile)
	description_experience = models.CharField(max_length=10000)
	proposal_file = models.FileField(upload_to="project_file", blank=True, null=True)
	expected_earning = models.IntegerField()
	expected_time = models.IntegerField()

#class Recommendations(models.Model):
#	recommendationer = models.ForeignKey('UserProfile', related_name = "recommendationer")
#	detail_name = models.CharField(max_length=50)
#	recommendation_type = models.CharField(max_length=1)
#	details = models.CharField(max_length=50)
#	recommendation_image = models.ImageField(upload_to="user_photo", default='user_photo/1.jpg')

class NewsFeed(models.Model):

	news_type= models.CharField(max_length=20, choices=(
		('Text And Photo', 'Text And Phto'),
		('New Project', 'New Project'),
		('Apply Project', 'Apply Project'),
		('Assigning Project', 'Assigning Project'),
		('Assigned Project', 'Assigned Project'),
		))
	user_profile = models.ForeignKey('UserProfile')

	text = models.CharField(max_length=1000, blank=True, null=True)
	image = models.ImageField(upload_to="news_feed_photo", blank=True, null=True)

	project = models.ForeignKey('Project', blank=True, null=True, default=None)
	application = models.ForeignKey('ProjectApplication', blank=True, null=True, default=None)

	event_date = models.DateTimeField(auto_now_add=True)

	#a list of users that have liked or disliked this project
	like = models.ManyToManyField(UserProfile, related_name="like")
	dislike = models.ManyToManyField(UserProfile, related_name="dislike")
	like_count = models.IntegerField(default=0)
	dislike_count = models.IntegerField(default=0)
