from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from . import views


urlpatterns = [
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/<str:social_type>", views.SocialLoginView.as_view(), name="social_login"),
    path("mypage", views.MypageView.as_view(), name="mypage"),
    path("introduction", views.UserIntroductionView.as_view(), name="introduction"),
]
