from django.db.models import ExpressionWrapper, OuterRef, Subquery, BooleanField, Value, Exists
from django.db.models.functions import Coalesce
from rest_framework import serializers
from rest_framework.serializers import HiddenField, CurrentUserDefault

from app.review.models import FoodTag, Product, Retailer, Review, Reaction, ReviewImage
from app.user.models import User, UserReviewBookmark, UserReviewLike


class ImageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["order", "url"]


class ReviewCreateSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    user = HiddenField(default=CurrentUserDefault())  # 현재 로그인한 유저를 작성자로 넣어주는거
    parent_review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), required=False, allow_null=True
    )  # 쿼리셋(모든리뷰)에해당 pk값을 가진 오브젝트가있는지validate에서확인한다
    reaction = serializers.PrimaryKeyRelatedField(required=True, queryset=Reaction.objects.all())
    food_tags = serializers.ListSerializer(child=serializers.CharField())
    retailer = serializers.CharField(allow_blank=True)  # validate역할:데이터가 char인지확인
    product = serializers.CharField(allow_blank=True)

    images = ImageSaveSerializer(many=True, required=False)

    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, attrs):
        retailer, _ = Retailer.objects.get_or_create(name=attrs["retailer"])
        product, _ = Product.objects.get_or_create(name=attrs["product"])
        attrs["retailer"] = retailer
        attrs["product"] = product

        return attrs

    def create(self, validated_data):
        images_data = validated_data.pop("images")
        food_tags_data = validated_data.pop("food_tags")
        parent_review = validated_data.get("parent_review")
        if parent_review:
            parent_review.quotation_count += 1
            parent_review.save()
        review = Review.objects.create(**validated_data)

        ReviewImage.objects.bulk_create(
            [ReviewImage(review=review, **image_data) for image_data in images_data]
        )

        food_tags = FoodTag.objects.filter(name__in=food_tags_data)
        review.food_tags.set(food_tags)
        return review


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "nickname", "profile_image", "tag"]

    def get_tag(self, obj):
        tag = obj.introduction_tags.get(step="1")
        return tag.name


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ParentReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "user", "reaction", "product", "description", "images", "is_updated"]

    def get_user(self, obj):
        return UserSerializer(instance=obj.user).data

    def get_reaction(self, obj):
        return ReactionSerializer(instance=obj.reaction).data

    def get_retailer(self, obj):
        return RetailerSerializer(instance=obj.retailer).data

    def get_product(self, obj):
        return ProductSerializer(instance=obj.product).data

    def get_images(self, obj):
        queryset = ReviewImage.objects.filter(review=obj)
        return ImageListSerializer(instance=queryset, many=True).data


class ReviewListSerializer(ParentReviewSerializer):
    user = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()
    retailer = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    parent_review = ParentReviewSerializer()

    class Meta:
        model = Review
        fields = "__all__"


class ReviewLikeSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    review = serializers.PrimaryKeyRelatedField(required=True, queryset=Review.objects.all())

    class Meta:
        model = UserReviewLike
        fields = "__all__"

    def validate(self, attrs):
        review = attrs["review"]
        user_review_like, created = UserReviewLike.objects.get_or_create(
            user=attrs["user"], review=review
        )
        if created:
            review.like_count += 1
            review.save()
        else:
            user_review_like.delete()
            review.like_count -= 1
            review.save()

        return attrs


class ReviewBookmarkSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    review = serializers.PrimaryKeyRelatedField(required=True, queryset=Review.objects.all())

    class Meta:
        model = UserReviewBookmark
        fields = "__all__"

    def validate(self, attrs):
        review = attrs["review"]
        user_review_bookmark, created = UserReviewBookmark.objects.get_or_create(
            user=attrs["user"], review=review
        )
        if created:
            review.bookmark_count += 1
            review.save()
        else:
            user_review_bookmark.delete()
            review.bookmark_count -= 1
            review.save()

        return attrs
