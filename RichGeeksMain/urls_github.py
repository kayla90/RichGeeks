from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^github$', 'RichGeeksMain.views_github.home', name='github'),
    url(r'^language/(?P<id>\d+)$', 'RichGeeksMain.views_github.language',name='language'),
    url(r'^sex/(?P<id>\d+)$', 'RichGeeksMain.views_github.sex'),
    url(r'^day_hour/(?P<id>\d+)$', 'RichGeeksMain.views_github.day_hour'),
    url(r'^get_language$', 'RichGeeksMain.views_github.language3'),
    url(r'^get_day_hour$', 'RichGeeksMain.views_github.get_day_hour'),
    url(r'^get_sex$', 'RichGeeksMain.views_github.get_sex'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)