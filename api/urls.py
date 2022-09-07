from django.urls import include, path

urlpatterns = [
    path("review/", include(("api.review.urls", "review"), namespace="review")),
    path("user/", include(("api.user.urls", "user"), namespace="user")),
    path("review/", include("api.review.urls")),
]
