from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound

from forms import *
from models import *


@login_required
def message(request):
	messages = Message.objects.filter(receiver__user=request.user).filter(is_active=True)
	return render(request, 'message.html', {'messages':messages})


@login_required
def send_message(request):
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'])

	form = SendMessageForm(request.POST)
	if not form.is_valid():
		return HttpResponseBadRequest()

	new_message = Message(
			sender=UserProfile.objects.get(user=request.user), 
			receiver=UserProfile.objects.get(user__id=form.cleaned_data['receiver_userid']),
			text=form.cleaned_data['message_content'])
	new_message.save()

	return HttpResponse()


@login_required
def reply_message(request):
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'])

	form = ReplyMessageForm(request.POST)
	if not form.is_valid():
		return HttpResponseNotBadRequest()

	new_message = Message(
			sender=UserProfile.objects.get(user=request.user),
			receiver=Message.objects.get(id=form.cleaned_data.ancestor_message_id).sender,
			ancestor=Message.objects.get(id=form.cleaned_data.ancestor_message_id),
			text=form.cleaned_data['message_content'])
	new_message.save()

	return HttpResponse()


@login_required
def delete_message(request, message_id):
	if not Message.objects.filter(id=message_id):
		return HttpResponseNotFound()

	message = Message.objects.get(id=message_id)
	message.is_active=False
	message.save()
	return redirect('/message')
