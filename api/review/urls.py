from django.urls import path

from . import views


urlpatterns = [
    path("", views.ReviewListCreateAPIView.as_view(), name="review_list_create"),
    path("image-presigned-url", views.PresignedUrlAPIView.as_view(), name="review-image-url"),
    path("like", views.ReviewLikeView.as_view(), name="review-like"),
    path("bookmark", views.ReviewBookmarkView.as_view(), name="review-bookmark"),
]
