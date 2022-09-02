from django.urls import path

from . import views


urlpatterns = [
    path("", views.ReviewListCreateAPIView.as_view(), name="review_list_create"),
    path("image-presigned-url", views.PresignedUrlView.as_view(), name="review-image-url"),
]
