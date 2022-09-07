import requests
from rest_framework.serializers import (
    CharField,
    BooleanField,
    Serializer,
    ModelSerializer,
    ListSerializer,
)
from rest_framework.serializers import HiddenField, CurrentUserDefault
from rest_framework_simplejwt.tokens import RefreshToken
from app.user.models import IntroductionTag, User, AuthUser


class UserRegisterSerializer(Serializer):
    social_id = CharField(label="소셜 아이디")
    social_type = CharField(label="소셜 타입")
    nickname = CharField(read_only=True, label="닉네임")
    is_new = BooleanField(read_only=False, label="신규유저 여부")
    access_token = CharField(read_only=True, label="토큰")
    refresh_token = CharField(read_only=True, label="리프레시")

    def validate(self, attrs):
        user = AuthUser.objects.get(
            social_id=attrs.get("social_id"), social_type=attrs.get("social_type")
        ).user
        nickname = user.nickname
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        attrs["nickname"] = nickname
        attrs["access_token"] = access_token
        attrs["refresh_token"] = refresh_token
        return attrs


class IntroductionSerializer(ModelSerializer):
    class Meta:
        model = IntroductionTag
        fields = "__all__"  # ["name"]


class UserIntroductionSerializer(ModelSerializer):
    introduction_tags = ListSerializer(child=CharField())
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = User
        fields = ["introduction_tags", "user"]

    def create(self, validated_data):
        print(validated_data["introduction_tags"])
        # tags = IntroductionTag.objects.filter(name__in=validated_data["introduction_tags"])
        datas = validated_data["introduction_tags"]
        for data in datas:
            user_tag, is_created = IntroductionTag.objects.get_or_create(
                name=data, defaults={"step": "3"}
            )

        tags = IntroductionTag.objects.filter(name__in=datas)
        user = validated_data["user"]
        user.introduction_tags.set(tags)
        return user
