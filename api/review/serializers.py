from rest_framework import serializers
from rest_framework.serializers import HiddenField, CurrentUserDefault

from app.review.models import Comment, FoodTag, Product, Retailer, Review, Reaction, ReviewImage
from app.user.models import User, UserReviewBookmark, UserReviewLike, IntroductionTag


class ImageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["order", "url"]


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


class ReviewCreateSerializer(serializers.ModelSerializer):

    user = HiddenField(default=CurrentUserDefault())
    parent_review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), required=False, allow_null=True
    )
    reaction = serializers.PrimaryKeyRelatedField(required=True, queryset=Reaction.objects.all())
    food_tags = serializers.ListSerializer(child=serializers.CharField())
    retailer = serializers.CharField(allow_blank=True)
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


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "profile_image"]


class ReviewCommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
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
