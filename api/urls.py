from django.urls import include, path

urlpatterns = [
    path("user/", include(("api.user.urls", "user"), namespace="user")),
    path("review/", include("api.review.urls")),
]
