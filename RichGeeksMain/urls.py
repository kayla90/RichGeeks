from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^home$', 'RichGeeksMain.views.home', name='home'),
    url(r'^news_feed$', 'RichGeeksMain.views.home', name='home'),
    url(r'^news_feed/like/(?P<news_feed_id>\d+)$', 'RichGeeksMain.views.like_news_feed'),
    url(r'^news_feed/dislike/(?P<news_feed_id>\d+)$', 'RichGeeksMain.views.dislike_news_feed'),
    url(r'^news_feed/post$', 'RichGeeksMain.views.post_news_feed'),
    url(r'^news_feed/photo/(?P<news_feed_id>\d+)$', 'RichGeeksMain.views.get_news_feed_photo'),

    url(r'^message$', 'RichGeeksMain.views.message'),
    url(r'^message/send$', 'RichGeeksMain.views.send_message'),
    url(r'^message/reply$', 'RichGeeksMain.views.reply_message'),  
    url(r'^message/delete/(?P<message_id>\d+)$', 'RichGeeksMain.views.delete_message'),  
    url(r'^message/number', 'RichGeeksMain.views.message_number'),

    url(r'^project/(?P<project_id>\d+)$', 'RichGeeksMain.views.project_detail', name='project'),
    url(r'^project/feedback/(?P<project_id>\d+)$', 'RichGeeksMain.views.feedback_project'),
    url(r'^project/evaluation/(?P<project_id>\d+)$', 'RichGeeksMain.views.evaluate_project'),
    url(r'^project/post$', 'RichGeeksMain.views.post_project', name='post_project'),
    url(r'^project/cancel/(?P<project_id>\d+)$', 'RichGeeksMain.views.cancel_project'),
    url(r'^project/apply/(?P<project_id>\d+)$', 'RichGeeksMain.views.apply_project'),
    url(r'^project/assign/(?P<project_id>\d+)/(?P<user_id>\d+)$', 'RichGeeksMain.views.assign_project'),
    url(r'^project/finish/(?P<project_id>\d+)$', 'RichGeeksMain.views.finish_project'),
    url(r'^market$', 'RichGeeksMain.views.market'),


)
