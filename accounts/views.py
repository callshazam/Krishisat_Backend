from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import FarmerRegistrationSerializer, StaffRegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
    

class FarmerRegistrationView(CreateAPIView):
    serializer_class = FarmerRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'status_code': status.HTTP_201_CREATED,
            'message': 'Farmer registered successfully',
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

class StaffRegistrationView(CreateAPIView):
    serializer_class = StaffRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            'success': True,
            'status_code': status.HTTP_201_CREATED,
            'message': 'Staff registered successfully',
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the tokens from the validated data
        access_token = serializer.validated_data['token']
        refresh_token = serializer.validated_data['refresh']
        user_type = serializer.validated_data['user_type']
        # user_id = serializer.validated_data['user_id']

        if user_type == "Superuser":
            message = 'Superuser logged in successfully'
        elif user_type == "Farmer":
            message = 'Farmer logged in successfully'
        elif user_type == "Staff":
            message = 'Staff logged in successfully'
        else:
            message = 'User logged in successfully'


        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': message,
            'user_type': user_type,
            # 'user_id': user_id,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        return Response(response, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
