from django.db import models
from app.core.models import TimeStamp


class FoodTag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "food_tags"


class Product(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "products"


class Retailer(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "retailers"


class Reaction(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "reactions"


class Review(TimeStamp):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    parent_review = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    reaction = models.ForeignKey("Reaction", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, blank=True)
    retailer = models.ForeignKey("Retailer", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    quotation_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    bookmark_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    is_updated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    food_tags = models.ManyToManyField("FoodTag", related_name="reviews")
    user_bookmarks = models.ManyToManyField(
        "user.User", related_name="bookmark_reviews", through="user.UserReviewBookmark"
    )
    user_likes = models.ManyToManyField(
        "user.User", related_name="like_reviews", through="user.UserReviewLike"
    )

    class Meta:
        db_table = "reviews"


class Comment(TimeStamp):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    like_count = models.IntegerField(default=0)
    is_updated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_likes = models.ManyToManyField(
        "user.User", related_name="comments", through="user.UserCommentLike"
    )

    class Meta:
        db_table = "comments"


class ReviewImage(models.Model):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    order = models.IntegerField()
    url = models.CharField(max_length=200)

    class Meta:
        db_table = "review_images"
