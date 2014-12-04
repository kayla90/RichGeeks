from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from forms import *
from models import *

@login_required
def market(request):
	projects = Project.objects.filter(status__in=['New','Open'])
	return render(request, 'market.html', {'projects':projects})


@login_required
def project_detail(request, project_id):
	if not Project.objects.filter(id=project_id):
		return HttpResponseNotFound("Project does not exist")

	project = Project.objects.get(id=project_id)
	content = {}
	print project.owner.user
	print request.user
	if (project.owner.user == request.user):
		print 'here'
		content['button'] = 'owner'

	content['project'] = project

	return render(request, 'project-detail.html', content)


@login_required
def feedback_project(request, project_id):
	if request.method != 'POST':
		return render(request, 'project-feedback.html', {})

	if not Project.objects.filter(id=project_id):
		return HttpResponseNotFound("Project does not exist")
	
	project = Project.objects.get(id=project_id)

	form = FeedbackProjectForm(request.POST)
	if not form.is_valid():
		return HttpResponseBadRequest("Input content not valid")
	
	new_feedback = ProjectFeedback(
			feedback_rating=form.cleaned_data['feedback_rating'],
			feedback_text=form.cleaned_data['feedback_text'])
	new_feedback.save()
	project.feedback.add(new_feedback)

	return redirect('/home')


@login_required
def evaluate_project(request, project_id):
	if request.method != 'POST':
		return render(request, 'project-evaluate.html', {'project_id':project_id})

	if not Project.objects.filter(id=project_id):
		return HttpResponseNotFound("Project does not exist")

	project = Project.objects.get(id=project_id)

	if project.owner.user != request.user:
		return HttpResponseBadRequest("You are not authorized to evaluate this project")

	if project.evaluated == True:
		return HttpResponseBadRequest("Project already evaluated")

	form = EvaluationProjectForm(request.POST)
	if not form.is_valid():
		return HttpResponseBadRequest("Input content not valid")

	project.evaluated = True
	project.evaluation_score = form.cleaned_data['evaluation_rating']
	project.evaluation_text = form.cleaned_data['evaluation_text']
	project.save()

	return redirect('/home')


@login_required
def post_project(request):

	context = {}
	if request.method != 'POST':
		return render(request, 'post-project.html', context)

	form = PostProjectForm(request.POST)
	if not form.is_valid():
		for i in form.errors:
			print i;
		return HttpResponseBadRequest("Input content not valid")
		#context['form'] = form
		#return render(request, 'post-project.html', context)

	new_project = Project(owner=UserProfile.objects.get(user=request.user),
			title=form.cleaned_data['title'],
			description=form.cleaned_data['description'],
			budget=form.cleaned_data['budget'],
			workload=form.cleaned_data['workload'],
			date_start=form.cleaned_data['date_start'],
			description_file=form.cleaned_data['description_file'])
	new_project.save()

	for item in form.cleaned_data['languages']:
		language = Languages(language=item)
		language.save()
		new_project.languages.add(language)
	new_project.save()

	new_news_feed = NewsFeed(news_type='New Project',
			user_profile=UserProfile.objects.get(user=request.user),
			project=new_project)
	new_news_feed.save()

	return redirect('/home')


@login_required
def cancel_project(request, project_id):
	
	if not Project.objects.filter(id=project_id):
		return HttpResponseNotFound("Project does not exist")

	project = Project.objects.get(id=project_id)

	if project.owner.user != request.user:
		return HttpResponseBadRequest("You are not authorized to cancel this project")

	project.status="Canceled"
	project.save()

	return redirect('/market')


@login_required
def apply_project(request, project_id):

	if not Project.objects.filter(id=project_id):
		return HttpResponseNotFound("Project does not exist")

	project = Project.objects.get(id=project_id)

	if request.method != 'POST':
		return render(request, 'project-apply.html', {'project_id':project_id})

	form = ApplyProjectForm(request.POST)
	if not form.is_valid():
		return HttpResponseBadRequest("Input content not valid")

	application = ProjectApplication(
			user_profile=UserProfile.objects.get(user=request.user),
			description_experience=form.cleaned_data['description_experience'],
			proposal_file=form.cleaned_data['proposal_file'],
			expected_earning=form.cleaned_data['expected_earning'],
			expected_time=form.cleaned_data['expected_time'])
	application.save()

	project.applications.add(application)
	project.save()

	message = Message(message_type="Apply Project", 
			sender=UserProfile.objects.get(user=request.user),
			receiver=project.owner,
			project=project,
			project_application=application)
	message.save()

	new_news_feed = NewsFeed(news_type='Apply Project',
			user_profile=UserProfile.objects.get(user=request.user),
			project=project,
			application=application)
	new_news_feed.save()
	
	return redirect('/market')


@login_required
def assign_project(request, project_id, user_id):

	if not Project.objects.filter(id=project_id):
		return HttpResponseNotFound("Project does not exist")

	project = Project.objects.get(id=project_id)

	if project.owner.user != request.user:
		return HttpResponseBadRequest("You are not authorized to assign this project")

	if project.assignee:
		return HttpResponseBadRequest("Project already assigned")

	if not User.objects.filter(id=user_id):
		return HttpResponseBadRequest("User does not exist")

	if not project.applications.filter(user_profile__user__id=user_id):
		return HttpResponseBadRequest("User didn't apply for this project")

	project.assignee = UserProfile.objects.get(user__id=user_id)
	project.status = "Working"
	project.save()

	application = ProjectApplication.objects.filter(user_profile__user__id=user_id).get(project=project)

	message = Message.objects.filter(project__id=project_id).get(sender__user__id=user_id)
	message.is_active=False
	message.save()

	new_message = Message(sender=UserProfile.objects.get(user=request.user),
			receiver=project.assignee,
			message_type='Assigned Project',
			project=project,
			project_application=application)
	new_message.save()

	new_news_feed_assigning = NewsFeed(news_type='Assigning Project',
			user_profile=UserProfile.objects.get(user=request.user),
			project=project,
			application=application)
	new_news_feed_assigning.save()

	new_news_feed_assigned = NewsFeed(news_type='Assigned Project',
			user_profile=UserProfile.objects.get(user__id=user_id),
			project=project,
			application=application)
	new_news_feed_assigned.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def finish_project(request, project_id):

	if not Project.objects.filter(id=project_id):
		return HttpResponseNotFound("Project does not exist")

	project = Project.objects.get(id=project_id)

	if project.owner.user != request.user:
		return HttpResponseBadRequest("You are not authorized to assign this project")

	if project.status!='Working':
		return HttpResponseBadRequest("Project not in the phase that can be completed")

	project.status='Completed'
	project.save()

	new_news_feed = NewsFeed(news_type="Project Complete",
			user_profile=project.assignee,
			project=project)
	new_news_feed.save()

	return redirect('/project/evaluation/'+project_id)
