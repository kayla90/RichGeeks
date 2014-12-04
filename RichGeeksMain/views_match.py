__author__ = 'renshiming'
from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from forms import *
from models import *
#def home(request):
#   return render(request, 'match.html')

def home(request):
    #recommendations.object.filter(recommendationer__user = request.user).delete()
    github_profiles = GitHubProfile.objects.get(githuber__user = request.user)
    user_language = github_profiles.language
    # project match
    language_list = []
    language_list.append(user_language)
    projects = Project.objects.filter(languages__language__in = language_list)
    #projects = projects.exclude(user_profile__user = request.user)
    if len(projects) > 6:
        projects = projects[:6] 
    n_project = len(projects)
    # teammate match
    teammates = GitHubProfile.objects.filter(language = user_language)
    teammates = teammates.exclude(githuber__user = request.user)
    if len(teammates) > 6:
        teammates = teammates[:6] 
    n_teammates = len(teammates)
    n_total = n_teammates + n_project
    context = {}
    context['teammates'] = teammates
    context['projects'] = projects
    return render(request, 'match.html', context)
