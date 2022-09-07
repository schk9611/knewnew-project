from django.urls import path

from api.review.views import ReviewDetail, CommentListCreateAPIView


urlpatterns = [
    path("<int:pk>/", ReviewDetail.as_view()),
    path("<int:pk>/comment/", CommentListCreateAPIView.as_view()),
]
