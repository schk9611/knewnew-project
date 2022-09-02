from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView
from . import views


urlpatterns = [
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("login/kakao", views.KakaoLoginView.as_view(), name="kakao_login"),
    path("introduction", views.UserIntroductionView.as_view(), name="introduction"),
]
