# Generated by Django 4.1 on 2022-08-30 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_alter_usercommentlike_table_and_more"),
        ("review", "0007_review_user_bookmarks_review_user_likes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="user_bookmarks",
            field=models.ManyToManyField(
                related_name="bookmark_reviews",
                through="user.UserReviewBookmark",
                to="user.user",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="user_likes",
            field=models.ManyToManyField(
                related_name="like_reviews",
                through="user.UserReviewLike",
                to="user.user",
            ),
        ),
    ]
