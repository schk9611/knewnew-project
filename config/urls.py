from django.urls import include, path

urlpatterns = [
    path("", include(arg=("api.urls", "api"), namespace="api")),
]
