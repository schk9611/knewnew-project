from rest_framework import generics

from app.review.models import Review, Comment

from api.review.serializers import (
    ReviewDetailSerializer,
    ReviewCommentSerializer,
    CommentCreateSerializer,
)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        return res


class CommentListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Comment.objects.filter(
            review_id=self.kwargs["pk"], parent_comment__isnull=True
        ).order_by("created_at")
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReviewCommentSerializer
        elif self.request.method == "POST":
            return CommentCreateSerializer
