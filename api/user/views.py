from json import JSONDecodeError
import requests

from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from app.user.models import User, AuthUser
from api.user.serializers import (
    UserRegisterSerializer,
    UserIntroductionSerializer,
)
from config.settings import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET


class SocialLoginView(GenericAPIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserRegisterSerializer

    def post(self, request, social_type, *args, **kwargs):
        try:
            if social_type == "kakao":
                token = request.headers.get("Authorization")
                profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {token}"},
                )
                profile_json = profile_request.json()
                kakao_account = profile_json.get("kakao_account")
                email = kakao_account.get("email")
                social_id = str(profile_json.get("id"))
                profile = kakao_account.get("profile")
                nickname = profile.get("nickname")
                profile_image = profile.get("profile_image_url")
                is_new = True
                social_type = social_type

            elif social_type == "naver":
                grant_type = "authorization_code"
                client_id = NAVER_CLIENT_ID
                client_secret = NAVER_CLIENT_SECRET
                code = request.GET.get("code")
                state = request.GET.get("state")
                parameter = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"

                token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?{parameter}")
                token_response_json = token_request.json()
                error = token_response_json.get("error", None)

                if error is not None:
                    raise JSONDecodeError(error)

                access_token = token_response_json.get("access_token")
                user_info_request = requests.get(
                    "https://openapi.naver.com/v1/nid/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                )

                naver_account = user_info_request.json().get("response")
                email = naver_account.get("email")
                social_id = naver_account.get("id")
                nickname = naver_account.get("nickname")
                profile_image = naver_account.get("profile_image")
                is_new = True
                social_type = social_type

            user, is_created = User.objects.get_or_create(
                email=email,
                defaults={"nickname": nickname, "profile_image": profile_image},
                headline=None,
                is_active=True,
            )
            if is_created:
                AuthUser.objects.create(user=user, social_id=social_id, social_type=social_type)
            else:
                if user.nickname != nickname:
                    user.nickname = nickname
                    user.save()
                if user.profile_image != profile_image:
                    user.profile_image = profile_image
                    user.save()
                if user.introduction_tags.exists():
                    is_new = False
            serializer = self.get_serializer(
                data=dict(social_id=social_id, social_type=social_type, is_new=is_new)
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

        except Exception as e:
            raise e


class UserIntroductionView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserIntroductionSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MypageView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        tags = self.request.user.introduction_tags.all()
        print(tags)
        return Response(
            {
                "nickname": user.nickname,
                "profile_image": user.profile_image,
                "introduction_tags": [tag.name for tag in tags],
            }
        )
