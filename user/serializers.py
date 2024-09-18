from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Farmer, Staff

class FarmerSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Farmer
        fields = ['id','user_name','password','farmer_name', 'phone_number', 'H_start_date', 'location', 'fpo_name', 'rice_type', 'water_source','geoJSON']
 
    def create(self, validated_data):
        # Extract user credentials
        user_name = validated_data.pop('user_name')
        password = validated_data.pop('password')

        # Authenticate the user with the provided credentials
        user = authenticate(username=user_name, password=password)

        if user is None:
            raise ValidationError("Invalid credentials. Please provide a valid username and password.")

        # Remove 'user' from validated_data if present
        validated_data.pop('user', None)  # Remove 'user' if it's in validated_data to avoid conflict

        # Create the Farmer instance with the authenticated user
        farmer = Farmer.objects.create(user=user, **validated_data)
        return farmer


class StaffCreateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ['user_name', 'password', 'name', 'phone_number', 'location', 'fpo_name']

    def create(self, validated_data):
        # Extract user credentials
        user_name = validated_data.pop('user_name')
        password = validated_data.pop('password')

        # Authenticate the user with the provided credentials
        user = authenticate(username=user_name, password=password)

        if user is None:
            raise ValidationError("Invalid credentials. Please provide a valid username and password.")

        # Check if the user is already assigned to a Staff member
        if Staff.objects.filter(user=user).exists():
            raise ValidationError("This user is already assigned to a staff member.")

        # Create the Staff instance with the authenticated user
        staff = Staff.objects.create(user=user, **validated_data)
        return staff

class StaffSerializer(serializers.ModelSerializer):
    added_farmers = FarmerSerializer(source='farmer_profile', many=True)

    class Meta:
        model = Staff
        fields = ['name', 'phone_number', 'location', 'fpo_name', 'added_farmers']

    def update(self, instance, validated_data):
        farmers_data = validated_data.pop('added_farmers', [])

        # Update added farmers
        current_farmers = instance.added_farmers.all()
        farmers_ids = [farmer.id for farmer in current_farmers]

        new_farmers = []
        for farmer_data in farmers_data:
            farmer_id = farmer_data.get('id')
            if farmer_id in farmers_ids:
                # Update existing farmer
                farmer = Farmer.objects.get(id=farmer_id)
                farmer.farmer_name = farmer_data.get('farmer_name', farmer.farmer_name)
                farmer.phone_number = farmer_data.get('phone_number', farmer.phone_number)
                farmer.H_start_date = farmer_data.get('H_start_date', farmer.H_start_date)
                farmer.location = farmer_data.get('location', farmer.location)
                farmer.fpo_name = farmer_data.get('fpo_name', farmer.fpo_name)
                farmer.rice_type = farmer_data.get('rice_type', farmer.rice_type)
                farmer.water_source = farmer_data.get('water_source', farmer.water_source)
                farmer.geoJSON = farmer_data.get('geoJSON', farmer.geoJSON)
                farmer.save()
            else:
                # Create a new farmer if no ID is present
                new_farmer = Farmer.objects.create(**farmer_data)
                instance.added_farmers.add(new_farmer)
                new_farmers.append(new_farmer)
                # Remove farmers that are no longer in the updated list
        for current_farmer in current_farmers:
            if current_farmer.id not in [farmer_data.get('id') for farmer_data in farmers_data]:
                instance.added_farmers.remove(current_farmer)

        return instance