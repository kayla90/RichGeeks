from views_message import *
from views_project import *
from views_news_feed import *

from django.shortcuts import render, redirect, get_object_or_404
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
def search(request, search):
	form = SearchForm(request.GET)
	if not form.is_valid():
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



