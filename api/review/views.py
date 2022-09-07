import os
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

import boto3

from . import serializers
from app.review.models import Review
from app.user.models import UserReviewLike


class ReviewListCreateAPIView(ListCreateAPIView):

    queryset = Review.objects.filter(is_active=True).order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ReviewListSerializer
        if self.request.method == "POST":
            return serializers.ReviewCreateSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PresignedUrlAPIView(APIView):
    def post(self, request):
        data = request.data
        file_name = data["fileName"]

        s3_client = boto3.client(
            "s3",
            region_name=os.environ.get("AWS_REGION_NAME"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
        )

        response = s3_client.generate_presigned_post(
            Bucket=os.environ.get("AWS_BUCKET_NAME"),
            Key=file_name,
            ExpiresIn=60,
            Fields={"acl": "public-read"},
            Conditions=[{"acl": "public-read"}],
        )

        return Response(response)


class ReviewLikeView(GenericAPIView):
    def get_serializer_class(self):
        return serializers.ReviewLikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"user": request.user.id, "review": request.data["review"]})


class ReviewBookmarkView(GenericAPIView):
    def get_serializer_class(self):
        return serializers.ReviewBookmarkSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"user": request.user.id, "review": request.data["review"]})
