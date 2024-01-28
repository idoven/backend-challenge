from rest_framework import status, viewsets
from connector import serializers
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


@extend_schema(tags=['user'])
class UserLoginView(APIView):
    """
    User login view
    """
    serializer_class = serializers.UserLoginSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='Request success'
            ),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
        request=serializer_class
    )
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


@extend_schema(tags=['user'])
class UserRegistrationView(APIView):
    """
    User registration view
    """
    serializer_class = serializers.UserRegistrationSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='Request success'
            ),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
        request=serializer_class
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['ecg_monitoring'])
class ECGView(viewsets.ViewSet, LoginRequiredMixin):
    """
    ECG Monitoring application service
    """
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
        """
        Receives ECG data for processing
        """
        pass

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='Request success', response=serializer_class_response
            ),
            404: OpenApiResponse(description='Resource not available'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
    )
    def retrieve(self):
        """
         Returns the number of times each ECG channel crosses zero
        """
        pass
