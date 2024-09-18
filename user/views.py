# views.py
from urllib import request
from rest_framework import generics
from rest_framework.views import APIView
from .models import Farmer, Staff
from .serializers import FarmerSerializer, StaffSerializer, StaffCreateSerializer
from .permissions import IsFarmer, SuperuserCanCreateStaffUser, IsStaff
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from django.contrib.auth import authenticate

class StaffCreateView(APIView):
    permission_classes = [IsAuthenticated,SuperuserCanCreateStaffUser]

    def post(self, request, *args, **kwargs):
        serializer = StaffCreateSerializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmerCreateView(generics.CreateAPIView):
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def perform_create(self, serializer):
        # Get the authenticated staff user
        staff_user = self.request.user

        # Ensure the authenticated user is linked to a staff instance
        try:
            staff = Staff.objects.get(user=staff_user)
        except Staff.DoesNotExist:
            raise ValidationError("Staff user not found.")

        # Extract the credentials from the request data
        user_name = self.request.data.get('user_name')
        password = self.request.data.get('password')

        # Authenticate the user
        user = authenticate(username=user_name, password=password)
        if user is None:
            raise ValidationError("Invalid credentials. Please provide a valid username and password.")

        # Save the farmer instance with both the staff and the authenticated user
        serializer.save(staff=staff, user=user)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class StaffDetailView(generics.RetrieveAPIView):  # staff list 
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated,IsStaff]

    def get_object(self):
        return Staff.objects.get(user=self.request.user)
    
class StaffUpdateFarmersView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated,IsStaff]

    def get_queryset(self):
        # Ensure the staff member only accesses their added farmers
        return Farmer.objects.filter(staff=self.request.user.staff_profile)

    def delete(self, request, pk, format=None):
        try:
            # Retrieve the Farmer instance using the primary key and check the staff
            farmer = Farmer.objects.get(pk=pk, staff=self.request.user.staff_profile)
            farmer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Farmer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class FarmerProfileView(generics.RetrieveAPIView):
    """
    View to retrieve the farmer's profile based on the logged-in user.
    """
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated,IsFarmer]

    def get_object(self):
        # Retrieve the farmer profile of the logged-in user
        try:
            farmer = Farmer.objects.get(user=self.request.user)
        except Farmer.DoesNotExist:
            raise NotFound("Farmer profile not found for this user.")
        
        return farmer