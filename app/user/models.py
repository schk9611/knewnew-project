from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from app.core.models import TimeStamp, CreatedTimeStamp
from app.review.models import Comment, Review


class User(TimeStamp, AbstractBaseUser):
    nickname = models.CharField(max_length=20)
    email = models.CharField(max_length=200, null=True, unique=True)
    profile_image = models.CharField(max_length=200, null=True)
    headline = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField()
    introduction_tags = models.ManyToManyField("IntroductionTag", related_name="users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"


class UserCommentLike(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        db_table = "users_comments_likes"


class AuthUser(TimeStamp):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    social_id = models.CharField(max_length=255)
    social_type = models.CharField(max_length=30)

    class Meta:
        db_table = "auth_users"


class IntroductionTag(models.Model):
    step = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "introduction_tags"


class UserReviewLike(CreatedTimeStamp):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        db_table = "users_reviews_likes"


class UserReviewBookmark(CreatedTimeStamp):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        db_table = "users_reviews_bookmarks"
