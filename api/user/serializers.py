import requests
from rest_framework.serializers import CharField, Serializer, ModelSerializer
from rest_framework.serializers import HiddenField, CurrentUserDefault
from rest_framework_simplejwt.tokens import RefreshToken
from app.user.models import IntroductionTag, User, AuthUser


class UserRegisterSerializer(Serializer):
    social_id = CharField(label="소셜 아이디")
    social_type = CharField(label="소셜 타입")

    def validate(self, attrs):
        user = AuthUser.objects.get(
            social_id=attrs.get("social_id"), social_type=attrs.get("social_type")
        ).user
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        attrs["refresh_token"] = refresh_token
        attrs["access_token"] = access_token
        return attrs


class IntroductionSerializer(ModelSerializer):
    class Meta:
        model = IntroductionTag
        fields = "__all__"


class UserIntroductionSerializer(ModelSerializer):
    introuction_tags = IntroductionSerializer(many=True)

    class Meta:
        model = User
        fields = ["introduction_tags"]

    def update(self, instance, validated_data):
        user = HiddenField(default=CurrentUserDefault())
        print(user)
        user_tags = validated_data.pop("introduction_tags")
        step = user_tags.get("step")
        name = user_tags.get("name")

        instance.step = IntroductionTag.objects.get(tag=step)
        instance.name = IntroductionTag.objects.get(name=name)
        instance.save()

        return instance
