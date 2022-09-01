from rest_framework import serializers

from app.review.models import FoodTag, Product, Retailer, Review, Reaction, ReviewImage
from app.user.models import User


class FoodTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTag
        fields = "__all__"


class ImageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["order", "url"]


class ReviewCreateSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        required=True, queryset=User.objects.all()
    )  # 쿼리셋에해당오브젝트가있는지validate에서확인
    parent_review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), required=False, allow_null=True
    )
    reaction = serializers.PrimaryKeyRelatedField(required=True, queryset=Reaction.objects.all())
    food_tags = FoodTagSerializer(many=True)
    retailer = serializers.CharField()  # validate역할:데이터가 char인지확인
    product = serializers.CharField()

    images = ImageSaveSerializer(many=True, required=False)

    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, attrs):
        print(attrs)
        retailer, _ = Retailer.objects.get_or_create(name=attrs["retailer"])
        product, _ = Product.objects.get_or_create(name=attrs["product"])
        attrs["retailer"] = retailer
        attrs["product"] = product

        return attrs

    def create(self, validated_data):
        images_data = validated_data.pop("images")
        food_tags_data = validated_data.pop("food_tags")

        review = Review.objects.create(**validated_data)

        for image_data in images_data:
            ReviewImage.objects.create(review=review, **image_data)

        food_tag_names = [food_tag_data["name"] for food_tag_data in food_tags_data]
        food_tags = FoodTag.objects.filter(name__in=food_tag_names)

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
