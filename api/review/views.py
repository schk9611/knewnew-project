import json
import os
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import boto3
import requests
from dotenv import load_dotenv

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


class PresignedUrlView(View):
    def post(self, request):
        load_dotenv()
        data = json.loads(request.body)
        OBJECT_NAME_TO_UPLOAD = data["fileName"]
        from botocore.client import Config

        s3_client = boto3.client(
            "s3",
            region_name="us-east-2",
            config=Config(signature_version="s3v4"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
        )

        # Generate the presigned URL
        response = s3_client.generate_presigned_post(
            Bucket="knewnew-review-images", Key=OBJECT_NAME_TO_UPLOAD, ExpiresIn=60
        )

        return JsonResponse({"results": response}, status=200)
