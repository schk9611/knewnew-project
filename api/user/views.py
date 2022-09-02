from logging import raiseExceptions
import requests
from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.review import serializers
from app.user.models import User, AuthUser

from api.user.serializers import UserRegisterSerializer, UserIntroductionSerializer


class KakaoLoginView(GenericAPIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            token = request.headers.get("Authorization")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {token}"}
            )
            print(profile_request)
            profile_json = profile_request.json()
            print(profile_json)
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email")
            social_id = str(profile_json.get("id"))
            profile = kakao_account.get("profile")
            nickname = profile.get("nickname")
            profile_image = profile.get("profile_image_url")
            social_type = "kakao"

            if not AuthUser.objects.filter(social_id=social_id).exists():
                user = User.objects.create(
                    email=email,
                    nickname=nickname,
                    profile_image=profile_image,
                    headline=None,
                    is_active=True,
                )
                AuthUser.objects.create(user=user, social_id=social_id, social_type=social_type)
            serializer = self.get_serializer(
                data=dict(social_id=social_id, social_type=social_type)
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

        except Exception as e:
            raise e


class UserIntroductionView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserIntroductionSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
