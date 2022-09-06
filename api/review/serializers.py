from rest_framework import serializers

from app.review.models import Comment, Review, ReviewImage
from app.user.models import User, IntroductionTag


class IntroductionTagSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroductionTag
        fields = ["name"]


class UserSimpleSerializer(serializers.ModelSerializer):
    introduction_tags = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "profile_image", "nickname", "introduction_tags"]

    def get_introduction_tags(self, obj):
        introduction_tag = obj.introduction_tags.filter(step="1")[0]
        return IntroductionTagSimpleSerializer(instance=introduction_tag).data


class FoodTagSimpleSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class ImageSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["order", "url"]


class ReviewDetailSerializer(serializers.ModelSerializer):
    parent_review_id = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    retailer = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    user = UserSimpleSerializer()
    food_tags = FoodTagSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "parent_review_id",
            "reaction",
            "product",
            "retailer",
            "description",
            "view_count",
            "quotation_count",
            "like_count",
            "bookmark_count",
            "share_count",
            "is_updated",
            "is_active",
            "created_at",
            "updated_at",
            "images",
            "food_tags",
            "user",
        ]

    def get_parent_review_id(self, obj):
        if obj.parent_review_id is not None:
            return obj.parent_review_id
        return ""

    def get_reaction(self, obj):
        return obj.reaction.name

    def get_product(self, obj):
        if obj.product is not None:
            return obj.product.name
        return ""

    def get_retailer(self, obj):
        return obj.retailer.name

    def get_images(self, obj):
        images = obj.reviewimage_set.all()
        return ImageSimpleSerializer(instance=images, many=True).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "profile_image"]


class ReviewCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    child_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "created_at",
            "like_count",
            "description",
            "user",
            "child_comments",
        ]

    def get_child_comments(self, obj):
        child = obj.comment_set.all().order_by("created_at")
        return ReviewCommentSerializer(instance=child, many=True).data


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ["review", "user", "parent_comment", "like_count", "description"]

    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), required=True)
    parent_comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False, allow_null=True
    )
    description = serializers.CharField(max_length=100)
