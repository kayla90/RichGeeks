from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from RichGeeksMain.models import *
from RichGeeksMain.forms import * 
from mimetypes import guess_type

@login_required
def home(request):
	news_feeds = NewsFeed.objects.all().order_by('-event_date')
	return render(request, 'home.html', {'news_feeds':news_feeds})


@login_required
def like_news_feed(request, news_feed_id):
	if not NewsFeed.objects.filter(id=news_feed_id):
		return HttpResponseNotFound("NewsFeed does not exist")

	news_feed = NewsFeed.objects.get(id=news_feed_id)

	current_user_profile = UserProfile.objects.get(user=request.user)
	if news_feed.like.filter(user=request.user):
		news_feed.like.remove(current_user_profile)
		news_feed.like_count = news_feed.like_count - 1
	else:
		news_feed.like.add(current_user_profile)
		news_feed.like_count = news_feed.like_count + 1
	
	news_feed.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_news_feed(request, news_feed_id):
	if not NewsFeed.objects.filter(id=news_feed_id):
		return HttpResponseNotFound("NewsFeed does not exist")

	news_feed = NewsFeed.objects.get(id=news_feed_id)

	current_user_profile = UserProfile.objects.get(user=request.user)
	if news_feed.dislike.filter(user=request.user):
		news_feed.dislike.remove(current_user_profile)
		news_feed.dislike_count = news_feed.dislike_count - 1
	else:
		news_feed.dislike.add(current_user_profile)
		news_feed.dislike_count = news_feed.dislike_count + 1
	
	news_feed.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def post_news_feed(request):
	if request.method == 'GET':
		return redirect('/news_feed')

	form = PostNewsFeedForm(request.POST, request.FILES)
	if not form.is_valid():
		return redirect('/news_feed')

	new_news_feed = NewsFeed(news_type='Text And Photo',
			user_profile=UserProfile.objects.get(user=request.user),
			text=form.cleaned_data['news_feed_text'],
			image=form.cleaned_data['image'])
	new_news_feed.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def get_news_feed_photo(request, news_feed_id):
	if not NewsFeed.objects.filter(id=news_feed_id):
		return HttpResponseNotFound()

	news_feed = NewsFeed.objects.get(id=news_feed_id)
	if not news_feed.image:
		print("no photo here")
		return HttpResponseNotFound()

	content_type = guess_type(news_feed.image.name)
	return HttpResponse(news_feed.image, content_type=content_type)
