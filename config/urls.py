from django.urls import path, include

urlpatterns = [
    path("", include(arg=("api.urls", "api"), namespace="api")),
]
