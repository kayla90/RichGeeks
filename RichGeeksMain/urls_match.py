from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^match$', 'RichGeeksMain.views_match.home', name='match'),
    url(r'^project_language$', 'RichGeeksMain.views_match.project_language'),
    url(r'^get_project_language$', 'RichGeeksMain.views_match.get_project_language'),
    url(r'^get_language_match$', 'RichGeeksMain.views_match.get_language'),
    url(r'^set_language$', 'RichGeeksMain.views_match.set_language'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)