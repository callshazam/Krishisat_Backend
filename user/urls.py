from django.urls import path
from .views import FarmerCreateView, StaffCreateView, StaffDetailView, StaffUpdateFarmersView, FarmerProfileView

urlpatterns = [
    path('farmer/', FarmerCreateView.as_view(), name='farmer-detail'),
    path('staff/', StaffCreateView.as_view(), name='staff-create'),
    path('staff/profile/', StaffDetailView.as_view(), name='staff-detail'),
    path('staff/added_farmers/<int:pk>/', StaffUpdateFarmersView.as_view(), name='staff-update-farmers'),
    path('farmer/profile/', FarmerProfileView.as_view(), name='farmer-profile'),
]
