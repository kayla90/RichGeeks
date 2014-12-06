from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import Http404
from django.db.models import Q
from RichGeeksMain.models import *
from RichGeeksMain.forms import * 
from mimetypes import guess_type

@login_required
def home(request):
	friends = Friend.objects.filter(source__user = request.user).values_list('target', flat=True)
	news_feeds = NewsFeed.objects.filter(
		Q(user_profile__user__id__in=friends) | 
		Q(user_profile__user__id=request.user.id)).order_by('-event_date')
	ongoing = Project.objects.filter(status='Working').\
		filter(Q(owner__user=request.user)\
		| Q(assignee__user=request.user))
	finished = Project.objects.filter(status='Completed').\
		filter(Q(owner__user=request.user)\
		| Q(assignee__user=request.user))
	owned = Project.objects.filter(owner__user=request.user)
	post_form = PostNewsFeedForm()

	return render(request, 'home.html', {'news_feeds': news_feeds,
		'ongoing': ongoing, 'finished': finished,
		'owned': owned, 'post_form': post_form})


@login_required
def like_news_feed(request, news_feed_id):
	
	news_feed = get_object_or_404(NewsFeed, id=news_feed_id)

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

	news_feed = get_object_or_404(NewsFeed, id=news_feed_id)

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

	news_feed = get_object_or_404(NewsFeed, id=news_feed_id)
	if not news_feed.image:
		raise Http404()

	content_type = guess_type(news_feed.image.name)
	return HttpResponse(news_feed.image, content_type=content_type)
