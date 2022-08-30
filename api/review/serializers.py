from rest_framework import serializers

from app.review.models import FoodTag, Product, Retailer, Review, Reaction, ReviewImage
from app.user.models import User


class FoodTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTag
        fields = ["name"]


class ReviewCreateSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # parent_review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())
    # reaction = serializers.PrimaryKeyRelatedField(
    #     required=True, queryset=Reaction.objects.all()
    # )  # 숫자값으로 들어옴 1/ 2/ 3/ 4

    # food tags 필수 텍스트로 받음 여러개 가능
    food_tags = serializers.SlugRelatedField(
        queryset=FoodTag.objects.all(), many=True, slug_field="name"
    )

    # retailer = 텍스트로받음 get_or_create
    # retailer = serializers.SlugRelatedField(queryset=Retailer.objects.all(), slug_field="name")
    retailer = serializers.CharField()

    # # product = 텍스트로받음 get_or_create
    # product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field="name")
    product = serializers.CharField()

    # images 여러개

    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, attrs):

        print(attrs["retailer"])
        retailer, created = Retailer.objects.get_or_create(name=attrs["retailer"])
        product, created = Product.objects.get_or_create(name=attrs["product"])
        attrs["retailer"] = retailer
        attrs["product"] = product

        return attrs


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
        # tag = obj.userintroductiontag_set.get(introduction_tag__step="1").introduction_tag
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
        fields = [
            "id",
            "user",
            "reaction",
            "retailer",
            "product",
            "description",
            "images",
            "parent_review",
            "view_count",
            "comment_count",
            "like_count",
            "bookmark_count",
            "is_updated",
        ]
