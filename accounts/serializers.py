from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
# StaffRegistration serializers

CustomUser = get_user_model()

class StaffRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','phone_number', 'user_name', 'password']

    def create(self, validated_data):
        # Create a new staff member with the staff role
        staff = CustomUser(
            phone_number=validated_data['phone_number'],
            user_name=validated_data['user_name'],
            is_staff=True
        )                                                                                           
        staff.set_password(validated_data['password'])
        staff.save()
        return staff


# FarmerRegistration serializers

class FarmerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','phone_number', 'user_name', 'password']

    def create(self, validated_data):
        # Create a new farmer with the default farmer role
        farmer = CustomUser(
            phone_number=validated_data['phone_number'],
            user_name=validated_data['user_name'],
            is_farmer = True
        )
        farmer.set_password(validated_data['password'])
        farmer.save()
        return farmer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        # Authenticate user
        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this phone number and password is not found.'
            )

        # Generate refresh token and access token
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_token = str(refresh)

        # Determine user_type
        if user.is_superuser:
            user_type = "Superuser"
        elif user.is_farmer:
            user_type = "Farmer"
        elif user.is_staff:
            user_type = "Staff"
        else:
            user_type = "User"


        return {
            'phone_number': user.phone_number,
            'token': access,
            'refresh': refresh_token,
            'user_type': user_type,
        }

