from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'RichGeeksMain.views_basic.index', name='index'),
    url(r'^login$', 'RichGeeksMain.views_basic.signin', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'RichGeeksMain.views_basic.register', name='register'),
	url(r'^confirm-registration/(?P<id>\d+)/(?P<token>[a-z0-9\-]+)$', 'RichGeeksMain.views_basic.confirm_registration', name='confirm'),
	url(r'^avatar/(?P<id>\d+)$', 'RichGeeksMain.views_basic.get_profile_image', name='avatar'),
	url(r'^profile/(?P<userid>\d+)$', 'RichGeeksMain.views_basic.profile', name='profile'),
	url(r'^profile-overview/(?P<userid>\d+)$', 'RichGeeksMain.views_basic.profile_overview', name='profile-overview'),
	url(r'^profile-analysis/(?P<userid>\d+)$', 'RichGeeksMain.views_basic.profile_analysis', name='profile-analysis'),
	url(r'^edit$', 'RichGeeksMain.views_basic.edit', name='edit'),
	url(r'^change-password$', 'RichGeeksMain.views_basic.change_password', name='change_password'),
	url(r'^forget-password$', 'RichGeeksMain.views_basic.forget_password', name='forget_password'),
    url(r'^reset-password/(?P<id>\d+)/(?P<token>[a-z0-9\-]+)$', 'RichGeeksMain.views_basic.reset_password', name='reset_password'),
)