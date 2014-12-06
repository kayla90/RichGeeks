__author__ = 'renshiming'
from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from forms import *
from models import *
from django.template.loader import render_to_string
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
# "id","order","score","weight","color","label"
# "FIS",1.1,59,0.5,"#9E0041","Fisheries"
# "MAR",1.3,24,0.5,"#C32F4B","Mariculture"
@csrf_exempt
def project_language(request):
    context = {}
    context['username'] = request.user.username
    projects = Project.objects.all()
    context['data'] = len(projects)
    #return HttpResponse(render_to_string('project_language.html', context))
    #return HttpResponse(render_to_string('profile-overview.html', { 'profile': profile }))
    return render(request, 'project_language.html', context)

@csrf_exempt
def get_project_language(request):
    context = {}
    data = []
    colors = ["#4776B4", "#5E4EA1", "#4D9DB4", "#EAF195", "#C7E89E", "#9CD6A4","#6CC4A4","#E1514B","#F47245","#FB9F59","#FEC574","#FAE38C","#9E0041","#C32F4B"]
    ls = ['JavaScript', 'Ruby', 'Java', 'PHP', 'Python', 'C++', 'C', 'Objective-C', 'C#', 'Shell', 'CSS', 'Perl']
    languages_set = {}
    count = 0

    for l in ls:
        line_l = {}
        line_l['id'] = l
        line_l['label'] = l
        line_l['color'] = colors[count%len(colors)]
        line_l['score'] = 0
        line_l['weight'] = 1
        languages_set[l] = line_l
        count = count + 1
    count = 0
    projects = Project.objects.all()
    for project in projects:
        languages = project.languages.all()
        for language in languages:
            language_name = language.language
            languages_set[language_name]['score'] = languages_set[language_name]['score'] + 1
            count = count + 1
    max = 0
    for key in languages_set.keys():
        if languages_set[key]['score'] > max:
            max = languages_set[key]['score']

    for key in languages_set.keys():
        line = languages_set[key]
        data.append(line)

    #line['id'] = "FIS"
    #line['score'] = 60
    #line['weight'] = 0.5
    #line['color'] = "#9E0041"
    #line['label'] = "Fisheries"
    #line2 = {}
    #line['id'] = "FIS2"
    #line2['score'] = 24
    #line2['weight'] = 0.5
    #line2['color'] = "#C32F4B"
    #line2['label'] = "Mariculture"
    #data.append(line)
    #data.append(line2)
    json.dumps(data)
    context['data'] = data
    context['count'] = max
    #return HttpResponse(json.dumps(context), content_type="application/json")
    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def set_language(request):
    language = request.POST.get('language')
    username = request.user.username
    github = GitHubProfile.objects.get(githuber__user__username = username)
    github.language = language
    github.save()
    context = {}
    context['success'] = 'success'
    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def get_language(request):
    username = request.user.username
    language = ""
    try:
        github = GitHubProfile.objects.get(githuber__user__username = username)
        language = github.language
    except:
        new_profile = UserProfile.objects.get(user__username = username)
        git_profile = GitHubProfile(githuber = new_profile, language = 'Python')
        git_profile.save()
        language = "Python"
    
    context = {}
    context['language'] = language
    return HttpResponse(json.dumps(context), content_type="application/json")













