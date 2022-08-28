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
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    retailer = models.ForeignKey("Retailer", on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    view_count = models.IntegerField(default=0)
    quotation_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    bookmark_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "reviews"


class ReviewFoodTag(models.Model):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    food_tag = models.ForeignKey("FoodTag", on_delete=models.CASCADE)

    class Meta:
        db_table = "review_food_tags"


class Comment(TimeStamp):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    like_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "comments"


class ReviewImage(models.Model):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    order = models.IntegerField()
    url = models.CharField(max_length=200)

    class Meta:
        db_table = "review_images"
