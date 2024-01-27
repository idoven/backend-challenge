from rest_framework import status, viewsets
from connector import serializers

from drf_spectacular.utils import OpenApiResponse, extend_schema


@extend_schema(tags=['ecg_monitoring'])
class ECGView(viewsets.ViewSet):
    serializer_class_response = serializers.ECGResponseSerializer
    serializer_class_request = serializers.ECGModelSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='Request success'
            ),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
        request=serializer_class_request
    )
    def create(self):
        pass

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='Request success',response=serializer_class_response
            ),
            404: OpenApiResponse(description='Resource not available'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
    )
    def retrieve(self):
        pass
