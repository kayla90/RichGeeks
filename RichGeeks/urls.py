from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('RichGeeksMain.urls')),
    url(r'^', include('RichGeeksMain.urls_basic')),
    url(r'^', include('RichGeeksMain.urls_github')),
    url(r'^', include('RichGeeksMain.urls_match')),
)
