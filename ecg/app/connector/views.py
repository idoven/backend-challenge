from rest_framework import status, viewsets
from connector import serializers
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from connector import operations


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
        # Other than admin that was required, this endpoint also can create/register users
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['ecg_monitoring'])
class ECGView(viewsets.ViewSet):
    """
    ECG Monitoring application service
    """

    permission_classes = (AllowAny,)

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
    def create(self, request):
        """
        Receives ECG data for processing
        """
        operations.ECGOperations().create_ecg_record(request.data)

        return Response(f'ECG record created successfully', status=status.HTTP_200_OK)

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
    def retrieve(self, request, ecg_id):
        """
         Returns the number of times each ECG channel crosses zero
        """
        response = operations.ECGOperations().get_zero_crossing_count(ecg_id)

        return Response({'zero_crossing_count': response}, status=status.HTTP_200_OK)
