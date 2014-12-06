from django.test import TestCase, Client
from models import *
from forms import *
import datetime

class UserModelTest(TestCase):

	def setUp(self):
		new_user = User.objects.create_user(username='testUser', email='test@andrew.cmu.edu', password='1234')
		new_user.save()

	def test_create_user(self):
		self.assertTrue(User.objects.all().count() == 1)
		new_user = User.objects.create_user(username='testUser2', email='test2@andrew.cmu.edu', password='1234')
		new_user.save()
		self.assertTrue(User.objects.all().count() == 2)
		# Check filter user by username
		self.assertTrue(User.objects.filter(username='testUser').count() == 1)
		self.assertTrue(User.objects.filter(username='testUser2').count() == 1)
		# Check filter user by email
		self.assertTrue(User.objects.filter(email='test@andrew.cmu.edu').count() == 1)
		self.assertTrue(User.objects.filter(email='test2@andrew.cmu.edu').count() == 1)

	def test_password_user(self):
		self.assertTrue(User.objects.all().count() == 1)
		current_user = User.objects.get(username='testUser')
		self.assertTrue(current_user.check_password('1234'))



class RegisterTest(TestCase):

	def setUp(self):
		new_user = User.objects.create_user(username='testUser', email='test@andrew.cmu.edu', password='1234')
		new_user.save()

	def test_Register_new_user(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}

		# Call the register method in view file
		response = client.post('/register', new_user_dict)

		# Assert request successful
		self.assertEqual(response.status_code, 200)
		# Assert if user object increase
		self.assertTrue(User.objects.all().count() == 2)
		self.assertEqual(User.objects.get(username='maxket').is_active, False)
		# Assert if associated data model created
		self.assertTrue(UserProfile.objects.all().count() == 1)
		self.assertTrue(GitHubProfile.objects.all().count() == 1)



class LoginTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)

	def test_active_user(self):
		client = Client()
		login_user = {'username':'maxket', 'password':'1234'}
		# Before set user active status to ture, all login request will render index page
		response_before_first  = client.post('/login', login_user)
		self.assertEqual(response_before_first.status_code, 200)
		response_before_second = client.post('/login', login_user)
		self.assertEqual(response_before_second.status_code, 200)
		self.assertTrue(response_before_second.content==response_before_first.content)

		# Then set active to true, login will redirect to home page
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()
		response_after = client.post('/login', login_user)
		# Becuase return is a redirect, so it should be 302, not 200
		self.assertEqual(response_after.status_code, 302)
		self.assertTrue(response_before_second.content != response_after.content)



class LogoutTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)

	def test_logout_user(self):
		client = Client()
		login_user = {'username':'maxket', 'password':'1234'}

		# Before client login, news_feed will redirect to login page
		response_before  = client.post('/news_feed')
		self.assertEqual(response_before.status_code, 302)

		# Then login, news_feed will render news_feed page
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()
		client.post('/login', login_user)
		response_after_login = client.post('/news_feed')
		self.assertEqual(response_before.status_code, 302)

		# Then after logout, news_feed will redirect to login page again
		client.post('/logout')
		response_after_logout = client.post('/news_feed', login_user)
		self.assertEqual(response_before.status_code, 302)

		# So before login and after login should be different
		# And before login and after logout should be same
		self.assertTrue(response_before.content != response_after_login.content)
		self.assertEqual(response_before.content, response_after_logout.content)



class ChangeProfileTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()

	def test_change_profile(self):
		client = Client()
		login_user = {'username':'maxket', 'password':'1234'}
		client.post('/login', login_user)
		current_user = User.objects.get(username='maxket')
		current_user_profile = UserProfile.objects.get(user=current_user)
		self.assertTrue(current_user_profile.full_name == None)
		self.assertTrue(current_user_profile.phone == None)
		self.assertTrue(current_user_profile.country == None)

		new_profile = {'full_name': 'test', 'phone': '123-456-7890', 'country': 'usa'}
		response = client.post('/edit', new_profile)
		self.assertEqual(response.status_code, 302)
		current_user_profile = UserProfile.objects.get(user=current_user)
		self.assertEqual(current_user_profile.full_name, 'test')
		self.assertEqual(current_user_profile.phone, '123-456-7890')
		self.assertEqual(current_user_profile.country, 'usa')



class ChangePasswordTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()

	def test_change_password(self):
		client = Client()
		login_user = {'username':'maxket', 'password':'1234'}
		client.post('/login', login_user)
		current_user = User.objects.get(username='maxket')
		current_user_profile = UserProfile.objects.get(user=current_user)
		# Check current password
		self.assertTrue(current_user.check_password('1234'))

		# Then change the password
		new_password = {'current': '1234', 'password1': '1320', 'password2': '1320'}
		response = client.post('/change-password', new_password)
		self.assertEqual(response.status_code, 302)
		current_user = User.objects.get(username='maxket')
		# Check whether the password changed
		self.assertTrue(current_user.check_password('1320'))



class GetProfileImgTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()

	def test_profile_img(self):
		client = Client()
		login_user = {'username':'maxket', 'password':'1234'}
		client.post('/login', login_user)
		current_user = User.objects.get(username='maxket')
		string = '/avatar/%d' % current_user.id
		response = client.post(string)
		self.assertTrue(response.status_code,400)



class PostProjectTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()

	def test_post_project(self):
		client = Client()
		login_user = {'username':'maxket', 'password':'1234'}
		client.post('/login', login_user)
		current_user = User.objects.get(username='maxket')

		datetime_obj = datetime.date(2014, 12, 12)
		project = {'title': 'testProject', 'budget': 100, 'workload': 40, 'description': 'test project', 'date_start': datetime_obj}
		response = client.post('/project/post', project)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(Project.objects.all().count() == 1)
		current_project = Project.objects.get(owner = current_user)
		self.assertEqual(current_project.title, 'testProject')
		self.assertEqual(current_project.budget, 100)
		self.assertEqual(current_project.workload, 40)
		self.assertEqual(current_project.description, 'test project')



class PostNewFeedTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()


	def test_send_message(self):
		client = Client()
		login_user = {'username':'maxket', 'password':'1234'}
		client.post('/login', login_user)
		current_user = User.objects.get(username='maxket')

		post_new_feed = {'news_feed_text': 'test new feed'}
		response = client.post('/news_feed/post', post_new_feed)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(NewsFeed.objects.all().count(), 1)

		currentProfile = UserProfile.objects.get(user = current_user)
		currentNewFeed = NewsFeed.objects.get(user_profile = currentProfile)
		self.assertEqual(currentNewFeed.text, 'test new feed')

class ApplyProjectTest(TestCase):

	def setUp(self):
		client = Client()
		new_user_dict = {'username':'maxket', 'email':'zxy1320@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)
		current_user = User.objects.get(username='maxket')
		current_user.is_active = True
		current_user.save()

		new_user_dict = {'username':'applyPerson', 'email':'apply@gmail.com', 'password1':'1234', 'password2':'1234'}
		response = client.post('/register', new_user_dict)
		current_user = User.objects.get(username='applyPerson')
		current_user.is_active = True
		current_user.save()

		login_user = {'username':'maxket', 'password':'1234'}
		client.post('/login', login_user)
		datetime_obj = datetime.date(2014, 12, 12)
		project = {'title': 'testProject', 'budget': 100, 'workload': 40, 'description': 'test project', 'date_start': datetime_obj}
		response = client.post('/project/post', project)

	def test_apply_project(self):
		client = Client()
		post_user = User.objects.get(username='maxket')
		login_user = {'username':'applyPerson', 'password':'1234'}
		apply_user = User.objects.get(username="applyPerson")
		client.post('/login', login_user)

		project = Project.objects.get(owner=post_user)
		apply_form = {'description_experience': 'test description experience', 'expected_earning': 200, 'expected_time': 20}
		string = '/project/apply/%d' % project.id 
		response = client.post(string, apply_form)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(project.applications.count()==1)
		application = ProjectApplication.objects.get(user_profile = UserProfile.objects.get(user=apply_user))
		self.assertEqual(application.expected_time, 20)
		self.assertEqual(application.expected_earning, 200)
		self.assertEqual(application.description_experience, 'test description experience')








