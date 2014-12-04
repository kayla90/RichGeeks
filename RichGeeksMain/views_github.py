__author__ = 'renshiming'
from django.shortcuts import render
from github import Github
from django.http import HttpResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
ACCESS_TOKEN = '8e87a4670383b27a163b8a020955b4761a6da3dc'
# Create your views here.
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
def home(request):
    return render(request, 'index.html')

def sex(request, username):
    context = {}
    context['username'] = username
    return render(request, 'sex.html',context)
from datetime import datetime
@csrf_exempt
def get_sex3(request):
    context = {}
    context['data'] = {}
    context['data']['lineChart'] = []
    context['data']['pieChart'] = []
    return HttpResponse(json.dumps(context), content_type="application/json")
@csrf_exempt
def get_sex(request):
    context = {}
    context['data'] = {}
    context['data']['lineChart'] = []
    ###################
    # this is the real part
    USER = request.POST.get('username')
    url = "https://api.github.com/repos/"
    url = url + USER + '/'
    client = Github(ACCESS_TOKEN, per_page=100)
    user = client.get_user(USER)
    repos = user.get_repos()
    count_day_time = {}
    count_day_time['day'] = 0
    count_day_time['night'] = 0
    for repo in repos:
        content_repo = {}
        name = repo.name
        content_repo['label'] = name
        content_repo['date'] = str(repo.created_at)[0:9]
        total = 0
        new_url = url + name + '/commits'+"?access_token=8e87a4670383b27a163b8a020955b4761a6da3dc"
        response = requests.get(new_url)
        result = response.json()
        for commit in result:
            total = total + 1
            c = commit['commit']['committer']
            time = datetime.strptime(c['date'], DATETIME_FORMAT)
            h = time.hour
            if h > 8 and h < 18:
                count_day_time['day'] = count_day_time['day'] + 1
            else:
                count_day_time['night'] = count_day_time['night'] + 1
        content_repo['value'] = total
        context['data']['lineChart'].append(content_repo)

        total = float(count_day_time['day']) + float(count_day_time['night'])
        day_percentage = float(count_day_time['day'])/total
        night_percentage = count_day_time['night']/total
        context['data']['pieChart'] = []
        content_day = {}
        content_day['color'] = 'red'
        content_day['description'] = 'This is your day-workder factor.'
        content_day['title'] = 'Day'
        content_day['value'] = day_percentage
        content_night = {}
        content_night['color'] = 'blue'
        content_night['description'] = 'This is your night-workder factor'
        content_night['title'] = 'Night'
        content_night['value'] = night_percentage
        context['data']['pieChart'].append(content_day)
        context['data']['pieChart'].append(content_night)
    return HttpResponse(json.dumps(context), content_type="application/json")

import numpy
@csrf_exempt
def get_day_hour(request):
    context = {}
    context['data'] = []
    USER = request.POST.get('username')
    url = "https://api.github.com/repos/"
    url = url + USER + '/'
    client = Github(ACCESS_TOKEN, per_page=100)
    user = client.get_user(USER)
    repos = user.get_repos()
    dict = numpy.zeros((7, 24))
    for repo in repos:
        name = repo.name
        new_url = url + name + '/commits'+"?access_token=8e87a4670383b27a163b8a020955b4761a6da3dc"
        response = requests.get(new_url)
        result = response.json()
        for commit in result:
            c = commit['commit']['committer']
            time = datetime.strptime(c['date'], DATETIME_FORMAT)
            day = time.weekday()
            hour = time.hour
            dict[int(day)][int(hour)] = dict[int(day)][int(hour)] + 1

    for i in range(7):
        for j in range(24):
            thiswork = {}
            thiswork['day'] = i + 1
            thiswork['hour'] = j + 1
            thiswork['value'] = dict[i][j]
            context['data'].append(thiswork)
    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def day_hour(request, username):
    context = {}
    context['username'] = username
    return render(request, 'day_hour.html',context)
@csrf_exempt
def language2(request,username):
    context = {}
    context['username'] = username
    client = Github(ACCESS_TOKEN, per_page=100)
    user = client.get_user(username)
    repos = user.get_repos()
    for r in repos:
        print r.full_name + " " + r.language
        commits = r.get_commits()
        count = 0
        for commit in commits:
            count = count + 1
        print count
    return render(request, 'language.html')


@csrf_exempt
def language3(request):
    USER = request.POST.get('username')
    client = Github(ACCESS_TOKEN, per_page=100)
    user = client.get_user(USER)
    repos = user.get_repos()
    context = {}
    context['data'] = []
    candidate_language = {}
    for r in repos:
        languages = r.get_languages()
        for key in languages:
            if key in candidate_language:
                candidate_language[key] = candidate_language[key] + languages[key]
            else:
                candidate_language[key] = languages[key]
    candidates = candidate_language
    for r in repos:
        content = {}
        content['State'] = r.full_name
        languages = r.get_languages()
        content['freq'] = {}
        for key in candidates:
            content['freq'][key] = 0
        for key in languages:
            if key in candidates:
                content['freq'][key] = languages[key]
        context['data'].append(content)
    return HttpResponse(json.dumps(context),content_type="application/json")

@csrf_exempt
def language(request, username):
    context = {}
    context['username'] = username
    return render(request, 'language.html',context)