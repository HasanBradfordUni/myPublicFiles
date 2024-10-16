# flashcards/settings.py

# ...

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cards.apps.CardsConfig",
]

# flashcards/urls.py


from django.contrib import admin

from django.urls import path, include


urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("cards.urls")),

]

# cards/urls.py

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="cards/base.html"),
        name="home"
    ),
]
