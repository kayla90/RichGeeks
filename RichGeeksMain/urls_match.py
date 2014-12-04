from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^match$', 'RichGeeksMain.views_match.home'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)