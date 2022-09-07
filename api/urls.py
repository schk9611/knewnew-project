from django.urls import include, path

from . import views

urlpatterns = [
    path("review/", include(("api.review.urls", "review"), namespace="review")),
    path("user/", include(("api.user.urls", "user"), namespace="user")),
]
