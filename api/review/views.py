from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from . import serializers
from app.review.models import Review


class ReviewListCreateAPIView(ListCreateAPIView):

    queryset = Review.objects.filter(is_active=True).order_by("-created_at")
    permission_classes = [AllowAny]
    # 로그인한애는 is authenticated 함수true반환

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ReviewListSerializer
        if self.request.method == "POST":
            return serializers.ReviewCreateSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
