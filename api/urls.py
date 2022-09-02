from xml.etree.ElementInclude import include
from django.urls import include, path

from . import views

urlpatterns = [
    path("user/", include(("api.user.urls", "user"), namespace="user")),
]
