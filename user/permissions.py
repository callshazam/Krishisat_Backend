from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    """
    Permission to allow only staff users to perform certain actions.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class SuperuserCanCreateStaffUser(permissions.BasePermission):
    """
    Permission to allow only superusers to create staff users.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            # Ensure only superusers can create staff users
            is_creating_staff_user = request.data.get('is_staff', False)
            return request.user.is_superuser if is_creating_staff_user else True
        return True

class IsFarmer(permissions.BasePermission):
    """
    Custom permission to only allow farmers to access their own profile.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and has a farmer profile
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'farmer_profile') and 
            obj.user == request.user
        )