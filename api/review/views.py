import os
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import boto3
from dotenv import load_dotenv

from . import serializers
from app.review.models import Review


class ReviewListCreateAPIView(ListCreateAPIView):

    queryset = Review.objects.filter(is_active=True).order_by("-created_at")
    # permission_classes = [AllowAny]
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


class PresignedUrlView(APIView):
    def post(self, request):
        load_dotenv()
        data = request.data
        file_name = data["fileName"]

        s3_client = boto3.client(
            "s3",
            region_name=os.environ.get("AWS_REGION_NAME"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
        )

        response = s3_client.generate_presigned_post(
            Bucket=os.environ.get("AWS_BUCKET_NAME"), Key=file_name, ExpiresIn=60
        )

        return Response(response)
